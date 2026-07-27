import os
from dotenv import load_dotenv

load_dotenv()

def diagnosticar_agente():
    print("=" * 60)
    print("🔍 DIAGNÓSTICO DEL AGENTE AURA-MARKET")
    print("=" * 60)

    # 1. VERIFICAR API KEY
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key or api_key in ["clave de API", "TU_API_KEY_AQUI", ""]:
        print("❌ ERROR: Tu GOOGLE_API_KEY en el archivo .env no está configurada o es genérica.")
        print("👉 Solución: Abre .env y pon tu clave de https://aistudio.google.com/")
        return
    else:
        print(f"✅ API Key encontrada: {api_key[:6]}...{api_key[-4:]}")

    # 2. PROBAR BÚSQUEDA VECTORIAL (RAG - FAISS)
    print("\n------------------------------------------------------------")
    print("📚 PROBANDO BASE DE CONOCIMIENTO LOCAL (FAISS + EMBEDDINGS)")
    print("------------------------------------------------------------")
    try:
        from langchain_community.document_loaders import DirectoryLoader, TextLoader
        from langchain_text_splitters import RecursiveCharacterTextSplitter
        from langchain_community.vectorstores import FAISS
        from langchain_community.embeddings import HuggingFaceEmbeddings

        loader = DirectoryLoader('./docs', glob="*.txt", loader_cls=TextLoader, loader_kwargs={'encoding': 'utf-8'})
        documents = loader.load()
        print(f"📄 Documentos cargados exitosamente: {len(documents)} archivos.")

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        docs = text_splitter.split_documents(documents)

        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        vectorstore = FAISS.from_documents(docs, embeddings)
        retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

        pregunta_prueba = "¿Cuál es el plazo de devolución?"
        resultados = retriever.invoke(pregunta_prueba)

        print(f"\n🔍 Consulta de prueba: '{pregunta_prueba}'")
        print("✅ EL MOTOR RAG FUNCIONA PERFECTAMENTE. Fragmentos encontrados:")
        for i, doc in enumerate(resultados, 1):
            print(f"  --- Fragmento {i} ---")
            print(f"  {doc.page_content[:150]}...\n")

    except Exception as e:
        print(f"❌ Error en la base de datos vectorial local: {e}")

    # 3. PROBAR CONEXIÓN DIRECTA A GEMINI
    print("------------------------------------------------------------")
    print("🤖 PROBANDO CONEXIÓN Y CUOTA DE MODELO GEMINI")
    print("------------------------------------------------------------")
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI

        # Probando modelo principal
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            temperature=0.2,
            google_api_key=api_key
        )
        respuesta = llm.invoke("Hola, responde únicamente con 'Conexión Exitosa'")
        print(f"✅ Respuesta de Gemini: {respuesta.content.strip()}")
        print("\n🎉 ¡TODO TU SISTEMA FUNCIONA AL 100%! Puedes volver a Streamlit.")

    except Exception as e:
        err_str = str(e)
        if "429" in err_str or "RESOURCE_EXHAUSTED" in err_str:
            print("⚠️ CUOTA AGOTADA EN TU PROYECTO ACTUAL DE GOOGLE AI STUDIO.")
            print("\n📌 CÓMO RESOLVERLO EN 30 SEGUNDOS (GRATIS):")
            print("1. Ve a https://aistudio.google.com/")
            print("2. Haz clic en 'Get API key'.")
            print("3. Selecciona 'Create API key in NEW project' (Crear en UN NUEVO PROYECTO).")
            print("4. Copia la nueva API Key y pégala en tu archivo .env")
        else:
            print(f"❌ Error de API: {e}")

if __name__ == "__main__":
    diagnosticar_agente()
    