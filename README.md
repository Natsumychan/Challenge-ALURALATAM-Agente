🤖 Asistente Virtual Corporativo AuraMarket - Agente IA con Streamlit + RAG

Agente Inteligente de Atención al Cliente y Soporte Corporativo para AuraMarket

Desarrollado para la gestión automatizada de políticas de envío, devoluciones, garantías y soporte en e-commerce.

📌 Tabla de Contenidos

📋 Descripción General

📸 Demostración e Interfaz

🎬 Video Tutorial y Demostración

✨ Características Principales

🏗️ Arquitectura del Sistema

🔄 Flujo de Funcionamiento (RAG Engine)

⚡ Tecnologías Principales

📁 Estructura del Proyecto

📄 Cobertura de Documentación de AuraMarket

🛠️ Instalación y Ejecución Local

🧪 Diagnóstico y Pruebas Automatizadas

🤖 Modelos de LLM y Embeddings Soportados

🚀 Roadmap y Mejoras Futuras

📝 Licencia

📋 Descripción General

Asistente Virtual AuraMarket es un agente conversacional de Inteligencia Artificial diseñado para atender las solicitudes de los clientes y colaboradores de AuraMarket, una plataforma e-commerce de rápido crecimiento.

El asistente actúa como un canal centralizado de atención al cliente en tiempo real mediante arquitectura RAG (Retrieval-Augmented Generation). Procesa e indexa la documentación oficial de la empresa (guías de envíos, políticas de devoluciones, términos y condiciones, avisos de privacidad y preguntas frecuentes) para responder con exactitud sin incurrir en alucinaciones de información.

[!NOTE]
🚧 Estado del Proyecto: Funcional y En Producción Local

El agente cuenta con un motor de búsqueda vectorial local FAISS, caché de recursos optimizado en Streamlit, fallback dinámico de modelos de lenguaje (Groq Llama 3.1 y Google Gemini 2.0 Flash) y un script automatizado de diagnóstico (test_agente.py).

📸 Demostración e Interfaz

🖼️ Interfaz Web Conversacional (Streamlit)

El chatbot ofrece una experiencia fluida e interactiva mediante una interfaz limpia de chat con almacenamiento de historial en la sesión del cliente:

+-----------------------------------------------------------------------+
| 🤖 Asistente Virtual AuraMarket                                       |
| Bienvenido. Haz tus preguntas sobre políticas de envío y garantías.   |
+-----------------------------------------------------------------------+
| 👤 Usuario: ¿Cuál es el plazo máximo para solicitar una devolución?   |
|                                                                       |
| 🤖 Asistente: De acuerdo con la Política de Devoluciones de           |
|    AuraMarket, cuentas con 30 días calendario a partir de la entrega   |
|    del producto. Debe conservar sus etiquetas originales.              |
+-----------------------------------------------------------------------+
| [Escribe tu pregunta sobre AuraMarket aquí...                       ] |
+-----------------------------------------------------------------------+


🎬 Video Tutorial y Demostración

A continuación se muestra el video guía interactivo donde se explica paso a paso el funcionamiento del sistema RAG, la integración de modelos y cómo interactuar con el agente en Streamlit:

💡 ¿Qué aprenderás en este video?

Instalación y Setup: Configuración del entorno virtual y carga de variables .env.

Indexación de Documentos: Cómo se procesan y convierten los .txt corporativos en vectores con FAISS.

Prueba del Agente: Consultas en vivo sobre envíos, garantías y devoluciones de AuraMarket.

Diagnóstico con test_agente.py: Verificación paso a paso del estado de las API Keys y la base de conocimiento.

(Nota: Reemplaza TU_VIDEO_ID en la URL de la imagen y el enlace con el ID de tu video publicado en YouTube, Loom o Vimeo).

✨ Características Principales

🧠 Arquitectura RAG Vectorial Local (FAISS): Indexa y procesa automáticamente archivos .txt corporativos mediante HuggingFace Embeddings (all-MiniLM-L6-v2) sin costo adicional de API para embeddings.

⚡ Sistema Dinámico de Fallback LLM: Conmutación automática según disponibilidad de claves de API entre Groq (llama-3.1-8b-instant) y Google Gemini (gemini-2.0-flash).

⚡ Indexación Eficiente y Caché de Recursos: Hace uso de @st.cache_resource de Streamlit para cargar los embeddings e indexar los vectores una sola vez en memoria, garantizando respuestas en milisegundos.

🛡️ Respuestas Guiadas y Grounded: Restringe al modelo a responder únicamente utilizando el contexto corporativo. En caso de no hallar la información, sugiere amablemente contactar a soporte@auramarket.com.

🔍 Script de Diagnóstico Automatizado: Incluye test_agente.py para probar la validez de API Keys, la carga de documentos, la segmentación (chunking), la búsqueda en FAISS y la conectividad directa con la API.

💬 Gestión de Memoria Conversacional: Mantención de historial de chat mediante st.session_state durante la interacción del usuario.

🏗️ Arquitectura del Sistema

El sistema sigue una estructura RAG modular orquestada por LangChain y presentada con Streamlit:

graph TD
    User([👤 Cliente / Usuario]) <-->|Chat Input / Output| StreamlitUI[🎨 Interfaz Web Streamlit]
    StreamlitUI <-->|Prompt Input| RAGChain[🔗 LangChain RAG Pipeline]

    subgraph RAG Engine Local
        DirectoryLoader[📄 DirectoryLoader docs/*.txt] --> TextSplitter[✂️ RecursiveCharacterTextSplitter]
        TextSplitter --> Embeddings[🔤 HuggingFace Embeddings all-MiniLM-L6-v2]
        Embeddings --> FAISSStore[(💾 FAISS Vectorstore)]
        FAISSStore <-->|Top 3 Semantic Search| Retriever[🔍 Retriever k=3]
    end

    subgraph LLM Provider Selector
        RAGChain --> Retriever
        RAGChain --> ProviderSelector{⚡ Multi-LLM Provider}
        ProviderSelector -->|Prioridad 1| Groq[🥇 Groq llama-3.1-8b-instant]
        ProviderSelector -->|Prioridad 2 / Fallback| Gemini[🥈 Google Gemini gemini-2.0-flash]
    end

    ProviderSelector -->|Respuesta Final| StreamlitUI


🔄 Flujo de Funcionamiento (RAG Engine)

El proceso de respuesta del asistente sigue 5 fases clave:

Carga e Ingesta de Documentos:

obtener_retriever() analiza la carpeta ./docs, cargando todos los archivos .txt en codificación UTF-8 mediante DirectoryLoader y TextLoader.

Segmentación Semántica (Chunking):

Los documentos se dividen en fragmentos de chunk_size=1000 caracteres con un traslape (chunk_overlap=200) mediante RecursiveCharacterTextSplitter.

Vectorización y Persistencia Local:

Cada bloque es convertido a vectores densos mediante el modelo local de código abierto all-MiniLM-L6-v2 de HuggingFace y almacenado en un índice en memoria FAISS.

Búsqueda y Recuperación (Retrieval):

Cuando el usuario envía una consulta, el retriever extrae los 3 fragmentos más relevantes (k=3) utilizando distancia de similitud coseno.

Síntesis y Respuesta Aumentada (Generation):

El System Prompt inyecta el contexto recuperado y la pregunta del usuario hacia el LLM seleccionado (Groq Llama 3.1 o Gemini 2.0 Flash), entregando una respuesta clara y profesional.

⚡ Tecnologías Principales

Frontend / Dashboard: Streamlit 1.x

Orquestador RAG: LangChain (langchain-core, langchain-community, langchain-text-splitters)

Base de Datos Vectorial: FAISS (faiss-cpu)

Modelo de Embeddings: HuggingFace Sentence Transformers (all-MiniLM-L6-v2)

Proveedores de LLM:

🥇 Groq API: llama-3.1-8b-instant (alta velocidad)

🥈 Google Generative AI: gemini-2.0-flash

Diagnóstico y Entorno: Python 3.10+, python-dotenv

📁 Estructura del Proyecto

AuraMarket-Agent/
├── docs/                         # Base de conocimientos corporativa (.txt)
│   ├── guia_envios.txt           # Tiempos de entrega, cobertura y costos
│   ├── politica_devoluciones.txt # Tiempos de garantía, reembolsos y condiciones
│   ├── politica_privacidad.txt   # Tratamiento de datos personales y Ley Habeas Data
│   ├── preguntas_frecuentes.txt  # Métodos de pago, facturación y seguimiento
│   └── terminos_condiciones.txt  # Condiciones legales y garantía de fábrica
├── app.py                        # Aplicación principal de Streamlit y pipeline RAG
├── test_agente.py                # Script de diagnóstico, validación de API y pruebas
├── .env                          # Variables de entorno (API Keys)
├── .env.example                  # Plantilla de variables de entorno
├── guia_agente_ia_auramarket.html # Presentación y diapositivas de la arquitectura
└── README.md                     # Documentación oficial del proyecto


📄 Cobertura de Documentación de AuraMarket

El agente está capacitado para resolver consultas de las siguientes áreas operativas:

Documento

Temas Cubiertos

Ejemplo de Pregunta Resuelta

guia_envios.txt

Tiempos de entrega, envíos gratis > $150.000 COP, cobertura nacional.

"¿Cuánto tarda en llegar un pedido a Medellín?"

politica_devoluciones.txt

Plazo de 30 días, estado de etiquetas, proceso de reembolso.

"¿Qué necesito para devolver una prenda defectuosa?"

politica_privacidad.txt

Ley 1581, retención de datos por 24 meses, derechos de titular.

"¿Cómo solicito la eliminación de mis datos?"

preguntas_frecuentes.txt

Métodos de pago (PSE, Tarjetas), facturación y rastreo de guía.

"¿Puedo pagar con tarjeta de crédito internacional?"

terminos_condiciones.txt

Garantía de fábrica (12 meses), términos legales de compra.

"¿Qué cubre la garantía de fábrica de AuraMarket?"

🛠️ Instalación y Ejecución Local

1. Clonar o descargar el repositorio

git clone https://github.com/tu-usuario/auramarket-agent.git
cd auramarket-agent


2. Crear y activar el entorno virtual

python -m venv venv

# En Windows (PowerShell):
.\venv\Scripts\activate

# En Linux / macOS:
source venv/bin/activate


3. Instalar dependencias

pip install streamlit langchain langchain-community langchain-core langchain-text-splitters faiss-cpu sentence-transformers python-dotenv langchain-groq langchain-google-genai


4. Configurar variables de entorno (.env)

Crea un archivo .env en la raíz del proyecto basándote en la plantilla:

# Claves de API (Configura al menos una de las dos)
GROQ_API_KEY=gsk_tu_clave_de_groq_aqui
GOOGLE_API_KEY=AIzaSy_tu_clave_de_google_aqui


💡 Nota: Puedes obtener una API Key gratuita de Groq en Groq Console o de Google en Google AI Studio.

5. Iniciar la aplicación

streamlit run app.py


Accede desde tu navegador web en: http://localhost:8501

🧪 Diagnóstico y Pruebas Automatizadas

El proyecto incluye una herramienta de diagnóstico para verificar que todos los componentes estén funcionando correctamente antes de lanzar la interfaz gráfica:

python test_agente.py


El script verifica automáticamente:

🔑 Existencia y formato válido de la GOOGLE_API_KEY o GROQ_API_KEY.

📚 Lectura correcta de archivos .txt en la carpeta ./docs.

✂️ Correcta división del texto (chunking) y generación de embeddings locales.

🔍 Búsqueda de similitud en el índice vectorial FAISS.

🤖 Conexión en vivo y generación de prueba con el modelo Gemini / Groq.

🤖 Modelos de LLM y Embeddings Soportados

Componente

Modelo / Tecnología

Tipo / Proveedor

Propósito

Embeddings

all-MiniLM-L6-v2

HuggingFace (Local)

Vectorización rápida sin consumo de API

Vector DB

FAISS

Facebook AI Similarity Search

Almacenamiento e índice de búsqueda local

LLM (Opción 1)

llama-3.1-8b-instant

Groq API

Inferencia ultrarrápida (Motor Principal)

LLM (Opción 2)

gemini-2.0-flash

Google AI Studio

Inferencia de alta capacidad y fallback

🚀 Roadmap y Mejoras Futuras

[ ] 📄 Soporte Multiformato: Ampliar la ingesta de documentos a archivos PDF y DOCX.

[ ] 💾 Persistencia de Índice FAISS: Guardar el índice vectorial en disco (faiss.write_index) para acelerar el inicio inicial.

[ ] 🌐 Despliegue Cloud: Publicación en Streamlit Community Cloud o Render con variables de entorno seguras.

[ ] 📊 Evaluación RAG (Ragas): Medición de métricas de fidelidad (faithfulness) y relevancia de respuestas.

📝 Licencia

Desarrollado para el sistema de atención al cliente de AuraMarket.

© 2026 AuraMarket. Todos los derechos reservados.