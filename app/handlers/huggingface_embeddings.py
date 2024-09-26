from flask import request, jsonify
from ..utilities.embeddings_utils import generate_huggingface_embeddings

def huggingface_embeddings():
    data = request.json
    text = data.get('text')
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    embeddings = generate_huggingface_embeddings(text)
    return jsonify({'embeddings': embeddings})