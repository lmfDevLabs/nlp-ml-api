from flask import request, jsonify
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer, PorterStemmer

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

def tokenizer(text):
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    tokens = nltk.word_tokenize(text.lower())
    return ' '.join(tokens)

def stemmizer(text):
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    stemmer = PorterStemmer()
    return ' '.join([stemmer.stem(word) for word in text.split()])

def lemmatizer(text):
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    lemmatizer = WordNetLemmatizer()
    return ' '.join([lemmatizer.lemmatize(word) for word in text.split()])

def remove_stopwords(text):
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    stop_words = set(stopwords.words('english'))
    return ' '.join([word for word in text.split() if word.lower() not in stop_words])

