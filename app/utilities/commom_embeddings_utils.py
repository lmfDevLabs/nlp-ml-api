# imports 
import numpy as np
# utils
from app.utilities.text_processing_utils import calculate_token_length
from app.utilities.openai_embeddings_utils import generate_openai_embeddings
from app.utilities.openai_utils import init_openai_connection

# init open ai
MAX_TOKENS = init_openai_connection()

# genera los embeddings para los chunks de los docs pdf
def generate_chunk_embeddings(car_model,processed_chunks):
    print("generate_chunk_embeddings")
    chunks_data = []
    for i, chunk in enumerate(processed_chunks):
        if chunk.strip():  # Verificar que el chunk no esté vacío
            print(f"Procesando chunk {i+1}/{len(processed_chunks)}: {chunk[:100]}...")
            chunk_embedding = safe_get_embedding(chunk, car_model, is_large_text=True)
            if not chunk_embedding:
                return {'success': False, 'message': 'No se pudieron generar embeddings'}
            if chunk_embedding:
                chunks_data.append({
                    "chunk_text": chunk,
                    "chunk_embedding": chunk_embedding
                })
            else:
                print(f"No se pudo generar el embedding para el chunk {i+1}")
    return chunks_data

# Función para obtener embedding de texto largo dividiendo en chunks si es necesario
def get_embedding_for_large_text(text, chunk_size=1000):
    print("get_embedding_for_large_text")
    try:
        chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
        embeddings = []
        for chunk in chunks:
            if chunk.strip():  # Verificar que el chunk no esté vacío
                embedding = generate_openai_embeddings(chunk)
                if embedding:
                    embeddings.append(embedding)

        if embeddings:
            avg_embedding = np.mean(embeddings, axis=0)
            return avg_embedding.tolist()
        else:
            return None
    except Exception as e:
        print(f"Error al generar embedding para chunks: {e}")
        return None

# Función para generar embeddings de manera segura considerando la longitud en tokens
def safe_get_embedding(chunk, product, is_large_text=False):
    print("safe_get_embedding")
    try:
        token_length = calculate_token_length(chunk)

        if token_length > MAX_TOKENS or is_large_text:
            embedding = get_embedding_for_large_text(chunk)
        else:
            embedding = generate_openai_embeddings(chunk)

        if embedding is None:
            print(f"Embedding no generado para {product}")
        return embedding
    except Exception as e:
        print(f"Error al generar embedding para {product}: {e}")
        return None

# calcula similitud entre emdeddings
def calculate_similarity(embedding1, embedding2):
    print("calculate_similarity")
    """Calcula la similitud coseno entre dos embeddings"""
    return 1 - cosine(embedding1, embedding2)

# busca embeddings cercanos en la db vectorial
def search_docs_products(user_embedding, product_data, top_n=5):
    print("search_docs_products")
    """Actualiza el ranking dinámico basado en la similitud de embeddings"""
    ranking = []
    for product in product_data:
        product_embedding = np.array(product['embedding']).astype('float32')
        similarity_score = calculate_similarity(user_embedding, product_embedding)
        ranking.append((product['title'], similarity_score))
    
    ranking.sort(key=lambda x: x[1], reverse=True)
    return ranking[:top_n]
