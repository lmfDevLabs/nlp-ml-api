from flask import request, jsonify
from ..utilities.text_utils import remove_stopwords, stemmizer, lemmatizer, tokenizer
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

def tokenize_text():
    data = request.json
    text = data.get('text')
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    tokenize_text = tokenizer(text)
    return jsonify({'tokenized_text': tokenize_text})

def stemmize_text():
    data = request.json
    text = data.get('text')
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    stemmized_text = stemmizer(text)
    return jsonify({'stemmized_text': stemmized_text})

def lemmatize_text():
    data = request.json
    text = data.get('text')
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    lemmatized_text = lemmatizer(text)
    return jsonify({'lemmatized_text': lemmatized_text})

# Preprocesamiento de texto
def preprocess_text(text):
    data = request.json
    text = data.get('text')
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    lemmatized_text = lemmatizer(text)
    stop_words = remove_stopwords(text)
    tokens = tokens(text)
    return ' '.join(tokens)

