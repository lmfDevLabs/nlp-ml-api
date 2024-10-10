# imports
import numpy as np
import faiss
from langchain.vectorstores import FAISS
from langchain.docstore import InMemoryDocstore
from langchain.schema import Document
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory

# utils
from app.utilities.openai_utils import init_openai_connection

# init open ai connection
MAX_TOKENS,embeddings,api_key = init_openai_connection()

# Generar respuesta utilizando la cadena de conversación en LangChain 
def generate_response_via_chain(user_question, relevant_json_docs):
    """
    Configura la cadena de conversación en LangChain, utilizando los resultados de la búsqueda y LLM.
    """
    try:
        # Configurar la cadena de conversación
        conversation_chain = setup_pdf_retrieval_chain(relevant_json_docs)

        # Crear el historial de chat vacío o extraído de la sesión, si es necesario
        chat_history = []

        # Generar la respuesta utilizando la cadena de conversación
        response = conversation_chain({
            "question": user_question, 
            # "chat_history": chat_history
        })

        return response.get('answer', "No se pudo obtener una respuesta.")
    except Exception as e:
        print(f"Error al generar la respuesta: {e}")
        return "Error al generar la respuesta."

# Configuración de la cadena de conversación usando LangChain y la data de los modelos
def setup_pdf_retrieval_chain(relevant_json_docs):

    # embeddings = embeddings(openai_api_key=api_key, model="text-embedding-3-small")

    # --- Embeddings de los chunks de los PDFs ---
    pdf_embeddings = []
    pdf_documents = []

    for relevan_json_doc in relevant_json_docs:
        for chunk_data in relevan_json_doc.get('chunks_data', []):
            chunk_text = chunk_data['chunk_text']
            chunk_embedding = chunk_data['chunk_embedding']
            pdf_embeddings.append(chunk_embedding)
            pdf_documents.append(Document(page_content=chunk_text, metadata={"source": f"{relevan_json_doc['Car_Make']} {relevan_json_doc['Car_Model']}"}))

    # Crear índice FAISS solo para los chunks de los PDFs
    pdf_embedding_vectors = np.array(pdf_embeddings).astype('float32')
    pdf_embedding_dimension = pdf_embedding_vectors.shape[1]
    pdf_index = faiss.IndexFlatL2(pdf_embedding_dimension)
    pdf_index.add(pdf_embedding_vectors)
    pdf_docstore = InMemoryDocstore({i: doc for i, doc in enumerate(pdf_documents)})

    pdf_vectorstore = FAISS(
        index=pdf_index,
        docstore=pdf_docstore,
        index_to_docstore_id={i: i for i in range(len(pdf_documents))},
        embedding_function=embeddings
    )

    # Crear la memoria de conversación
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    
    # Crear la cadena de conversación para PDFs (Recuperación de contenido basado en los PDFs)
    llm = ChatOpenAI(openai_api_key=api_key)
    pdf_conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=pdf_vectorstore.as_retriever(),
        memory=memory
    )

    return pdf_conversation_chain