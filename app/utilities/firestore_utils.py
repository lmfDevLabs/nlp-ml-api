from flask import request, jsonify
import numpy as np
import json
import os
from google.cloud import storage

# Cargar embeddings desde Cloud Storage
def load_embeddings_from_storage(bucket_name, file_path):
    try:
        client = storage.Client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(file_path)
        temp_file_path = os.path.join('/tmp', file_path)
        blob.download_to_filename(temp_file_path)

        with open(temp_file_path, 'r') as f:
            embeddings_data = json.load(f)

        return embeddings_data

    except Exception as e:
        print(f'Error loading embeddings: {e}')
        return None