import numpy as np
# from langchain_community.embeddings import OpenAIEmbeddings
from langchain_openai import OpenAIEmbeddings
# utils
from app.utilities.text_processing_utils import calculate_token_length
from app.utilities.openai_utils import init_openai_connection

# init open ai connection
MAX_TOKENS,embeddings,api_key = init_openai_connection()

# Inicializar la clase OpenAIEmbeddings de Langchain
def generate_openai_embeddings(text):
    print("generate_openai_embeddings")
    try:
        embeddings_model = embeddings(openai_api_key=api_key)
        # Usar OpenAIEmbeddings de Langchain para generar embeddings
        #embeddings_model = OpenAIEmbeddings(openai_api_key=api_key)
        embeddings = embeddings_model.embed_query(text)
        return embeddings
    except Exception as e:
        print(f"Error al generar embeddings con Langchain: {e}")
        return None

