import os
# from langchain_community.embeddings import OpenAIEmbeddings
from langchain_openai import OpenAIEmbeddings

# Configuración de API y Embeddings
def init_openai_connection():
    
    # Asegúrate de configurar tu clave de API de OpenAI
    api_key = os.getenv('OPENAI_API_KEY')

    # Inicializar embeddings de OpenAI
    if api_key is None:
        print("Error: No se encontró la API key de OpenAI. Asegúrate de que esté configurada en la variable de entorno 'OPENAI_API_KEY'.")
    else:
        embeddings = OpenAIEmbeddings(openai_api_key=api_key, model="text-embedding-3-small")

    MAX_TOKENS = 8192

    return MAX_TOKENS,embeddings,api_key


