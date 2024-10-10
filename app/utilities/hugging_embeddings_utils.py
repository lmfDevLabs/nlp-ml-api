from flask import request, jsonify
from transformers import AutoTokenizer, AutoModel

def generate_huggingface_embeddings(text):
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    tokenizer = AutoTokenizer.from_pretrained("hkunlp/instructor-large")
    model = AutoModel.from_pretrained("hkunlp/instructor-large")
    inputs = tokenizer(text, return_tensors="pt")
    outputs = model(**inputs)
    embeddings = outputs.last_hidden_state.mean(dim=1).detach().numpy().tolist()
    return embeddings