# packages
from flask import Blueprint, request, jsonify
# handlres
from .handlers.vector_operations import vector_distance
from .handlers.text_processing import tokenize_text, lemmatize_text, stemmize_text 
from .handlers.openai_embeddings import openai_embeddings
from .handlers.huggingface_embeddings import huggingface_embeddings

main_bp = Blueprint('main', __name__)

#routes
@main_bp.route('/text/tokenize', methods=['POST'])
def tokenize_text_route():
    return tokenize_text()

@main_bp.route('/text/lemmatize', methods=['POST'])
def lemmatize_text_route():
    return lemmatize_text()

@main_bp.route('/text/stemmize', methods=['POST'])
def stemmize_text_route():
    return stemmize_text()

@main_bp.route('/embeddings/openai', methods=['POST'])
def openai_embeddings_route():
    return openai_embeddings()

@main_bp.route('/embeddings/huggingface', methods=['POST'])
def huggingface_embeddings_route():
    return huggingface_embeddings()

@main_bp.route('/vector/distance', methods=['POST'])
def vector_distance_route():
    # from req
    data = request.get_json()
    query_embedding = data.get('query_embedding')
    embeddings_data = data.get('embeddings_data')
    return vector_distance(query_embedding, embeddings_data, top_k=5)

@main_bp.route('/test-connection', methods=['GET'])
def test_connection():
    return jsonify({'message': 'Connection successful!'}), 200