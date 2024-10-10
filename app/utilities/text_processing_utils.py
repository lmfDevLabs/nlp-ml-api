from flask import request, jsonify
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer, PorterStemmer
import tiktoken

# paquetes nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')


## LESS THAN WORDS
# Función para calcular la longitud en tokens
def calculate_token_length(text):
    encoding = tiktoken.encoding_for_model("text-embedding-3-small")
    return len(encoding.encode(text))

## WORDS
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


## PARAGRAPHS
# Función para dividir el texto en párrafos
def split_text_into_paragraphs(text):
    paragraphs = text.split('\n\n')
    return [p.strip() for p in paragraphs if p.strip()]

# Función para dividir los párrafos en chunks basados en la longitud de tokens
def chunk_paragraphs(paragraphs, max_tokens=1600):
    chunks = []
    current_chunk = []
    current_tokens = 0

    for paragraph in paragraphs:
        paragraph_tokens = calculate_token_length(paragraph)
        if current_tokens + paragraph_tokens > max_tokens:
            chunks.append(' '.join(current_chunk))
            current_chunk = [paragraph]
            current_tokens = paragraph_tokens
        else:
            current_chunk.append(paragraph)
            current_tokens += paragraph_tokens

    if current_chunk:
        chunks.append(' '.join(current_chunk))

    return chunks


# BUYERS
# Extraer palabras clave de los mensages de los usuarios
def preprocess_text_and_create_tags(text):
    """Procesa el texto y extrae palabras clave eliminando stopwords"""
    doc = nlp(text.lower())
    keywords = [token.lemma_ for token in doc if token.text not in stop_words and token.is_alpha]
    return keywords