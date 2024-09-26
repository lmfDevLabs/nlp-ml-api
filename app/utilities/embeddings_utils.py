import os
from flask import request, jsonify
import openai
from langchain.embeddings import OpenAIEmbeddings
from transformers import AutoTokenizer, AutoModel


# Asegúrate de configurar tu clave de API de OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')

def generate_openai_embeddings(text):
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    embeddings = OpenAIEmbeddings()
    return embeddings.embed(text)

def generate_huggingface_embeddings(text):
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    tokenizer = AutoTokenizer.from_pretrained("hkunlp/instructor-large")
    model = AutoModel.from_pretrained("hkunlp/instructor-large")
    inputs = tokenizer(text, return_tensors="pt")
    outputs = model(**inputs)
    embeddings = outputs.last_hidden_state.mean(dim=1).detach().numpy().tolist()
    return embeddings