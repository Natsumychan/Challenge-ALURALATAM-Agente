import os
import streamlit as st
from dotenv import load_dotenv

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# Cargar variables de entorno del archivo .env
load_dotenv()

st.set_page_config(
    page_title="Agente IA AuraMarket",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 Asistente Virtual AuraMarket")
st.write("Bienvenido. Haz tus preguntas sobre políticas de envío, devoluciones y garantías.")

@st.cache_resource(show_spinner="Indexando base de conocimiento local de AuraMarket...")
def obtener_retriever():
    """Carga los documentos .txt y genera el almacén de vectores FAISS localmente."""
    docs_path = "./docs"
    if not os.path.exists(docs_path) or not os.listdir(docs_path):
        raise FileNotFoundError(
            "La carpeta './docs' no existe o está vacía. Añade tus archivos .txt."
        )

    # 1. Cargar documentos de texto con codificación UTF-8
    loader = DirectoryLoader(
        docs_path,
        glob="*.txt",
        loader_cls=TextLoader,
        loader_kwargs={'encoding': 'utf-8'}
    )
    documents = loader.load()

    # 2. Dividir texto en bloques
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = text_splitter.split_documents(documents)

    # 3. Embeddings locales (Sin costo de API)
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(docs, embeddings)
    return vectorstore.as_retriever(search_kwargs={"k": 3})

def obtener_llm():
    """Selecciona el proveedor LLM disponible (Groq o Gemini)."""
    groq_key = os.getenv("GROQ_API_KEY")
    google_key = os.getenv("GOOGLE_API_KEY")

    # Opción 1: Prioridad a Groq (Llama 3.1) si está disponible
    if groq_key and not groq_key.startswith("TU_"):
        try:
            from langchain_groq import ChatGroq
            st.sidebar.success("⚡ Motor activo: Groq (Llama 3.1)")
            return ChatGroq(
                model_name="llama-3.1-8b-instant",
                groq_api_key=groq_key,
                temperature=0.2
            )
        except ImportError:
            st.warning("Para usar Groq instala la librería: `pip install langchain-groq`")

    # Opción 2: Usar Gemini si la API key de Google está presente
    if google_key and not google_key.startswith("TU_"):
        try:
            from langchain_google_genai import ChatGoogleGenerativeAI
            st.sidebar.info("🤖 Motor activo: Google Gemini 2.0")
            return ChatGoogleGenerativeAI(
                model="gemini-2.0-flash",
                temperature=0.2,
                google_api_key=google_key
            )
        except Exception:
            pass

    raise ValueError(
        "No se encontró una API Key válida. Configura `GROQ_API_KEY` o `GOOGLE_API_KEY` en tu archivo `.env`."
    )

def invocar_agente(retriever, llm, prompt_usuario):
    system_prompt = (
        "Eres un agente corporativo amigable de atención al cliente de AuraMarket.\n"
        "Responde a las preguntas utilizando únicamente el siguiente contexto proporcionado.\n"
        "Si no encuentras la respuesta en el contexto, indica amablemente que no dispones "
        "de esa información y ofrece contacto con soporte@auramarket.com.\n\n"
        "Contexto:\n{context}\n\n"
        "Pregunta: {input}"
    )
    prompt = ChatPromptTemplate.from_template(system_prompt)

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    rag_chain = (
        {"context": retriever | format_docs, "input": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain.invoke(prompt_usuario)

try:
    retriever = obtener_retriever()
    llm = obtener_llm()

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Mostrar historial de conversación
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Captura de entrada del usuario
    if prompt_usuario := st.chat_input("Escribe tu pregunta sobre AuraMarket aquí..."):
        st.session_state.messages.append({"role": "user", "content": prompt_usuario})
        with st.chat_message("user"):
            st.markdown(prompt_usuario)

        with st.chat_message("assistant"):
            with st.spinner("Consultando información de AuraMarket..."):
                try:
                    respuesta = invocar_agente(retriever, llm, prompt_usuario)
                    st.markdown(respuesta)
                    st.session_state.messages.append({"role": "assistant", "content": respuesta})
                except Exception as ex:
                    st.error(f"Error procesando la solicitud: {ex}")

except Exception as e:
    st.error(f"⚠️ Error de inicialización: {e}")
    st.info(
        "💡 **Para resolverlo:**\n"
        "1. Consigue una API Key gratis en [Console Groq](https://console.groq.com/keys).\n"
        "2. Ejecuta en consola: `pip install langchain-groq`.\n"
        "3. Añade `GROQ_API_KEY=gsk_...` a tu archivo `.env`."
    )
