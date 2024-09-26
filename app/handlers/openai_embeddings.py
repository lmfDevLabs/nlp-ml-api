from flask import request, jsonify
from ..utilities.embeddings_utils import generate_openai_embeddings

def openai_embeddings():
    data = request.json 
    text = data.get('text')
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    embeddings = generate_openai_embeddings(text)
    return jsonify({'embeddings': embeddings})