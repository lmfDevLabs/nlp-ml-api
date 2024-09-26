from flask import request, jsonify
import numpy as np
import json
import os
from google.cloud import storage

# Buscar en embeddings
def vector_distance(query_embedding, embeddings_data, top_k=5):
    if not query_embedding or not embeddings_data:
        return jsonify({'error': 'Invalid input data'}), 400

    embeddings_matrix = np.array([item['embedding'] for item in embeddings_data])
    
    distances = np.linalg.norm(embeddings_matrix - query_embedding, axis=1)
    nearest_indices = distances.argsort()[:top_k]
    
    results = [embeddings_data[idx] for idx in nearest_indices]
    return results
