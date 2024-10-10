import os
import json
from threading import Lock
from firebase_admin import storage
from google.cloud import storage

# SELLERS
# Cargar base de datos de PDFs embebidos (vector store) desde Cloud Storage - sin uso
def download_docs_embeddings_from_gcs(file_path):
    print("download_docs_embeddings_from_gcs")
    try:
        # Inicializar el cliente de Google Cloud Storage
        storage_client = storage.Client()

        # Obtener el bucket de Cloud Storage
        bucket = storage.bucket()

        # Obtener el blob (archivo) que queremos descargar
        blob = bucket.blob(file_path)

        # Descargar el archivo y cargarlo en memoria
        downloaded_json = blob.download_as_string()

        # Convertir la cadena descargada en un objeto JSON
        pdf_embeddings = json.loads(downloaded_json)
        return pdf_embeddings
    
    except Exception as e:
        print(f"Error al cargar los embeddings de PDFs desde Cloud Storage: {e}")
        return []

# para subir archivo de embeddings a cs
def upload_seller_embeddings_to_gcs(seller_id, company_name, show_room_id, embeddings_data):
    print("upload_embeddings_to_storage")
    
    # vars
    json_file_path = f"{show_room_id}/docs_sellers/{seller_id}/{seller_id}-{company_name}-embeddings.json"
    temp_file_path = os.path.join(os.path.dirname(__file__), f"{seller_id}.json")

    try:
        mutex = Lock()
        mutex.acquire()
        bucket = storage.bucket()

        # Verificar si el archivo ya existe en Cloud Storage
        blob = bucket.blob(json_file_path)
        if blob.exists():
            # Descargar el archivo y agregar los nuevos embeddings
            blob.download_to_filename(temp_file_path)
            with open(temp_file_path, "r") as f:
                existing_data = json.load(f)
        else:
            existing_data = []

        # Actualizar el archivo con los nuevos embeddings
        existing_data.append(embeddings_data)
        with open(temp_file_path, "w") as f:
            json.dump(existing_data, f, indent=2)

        # Subir de nuevo el archivo actualizado
        blob.upload_from_filename(temp_file_path)
        print('Embeddings subidos exitosamente.')

    except Exception as e:
        print(f"Error al subir embeddings: {e}")
    finally:
        mutex.release()

# para subir consolidado de embeddings a gcs
def upload_consolidate_embeddings_to_gcs(consolidated_file_path, current_data):
    try:
        # Inicializar el cliente de Google Cloud Storage
        storage_client = storage.Client()

        # Obtener el bucket de Cloud Storage (debes definir el nombre de tu bucket)
        bucket_name = 'your-bucket-name'  # Reemplaza con el nombre de tu bucket
        bucket = storage_client.bucket(bucket_name)

        # Crear un blob (archivo) en la ubicación especificada
        blob = bucket.blob(consolidated_file_path)

        # Convertir los datos a una cadena JSON
        json_data = json.dumps(current_data, indent=4)

        # Subir el archivo JSON a Cloud Storage
        blob.upload_from_string(json_data, content_type='application/json')

        print(f"Archivo {consolidated_file_path} subido con éxito a Cloud Storage")
        return {'success': True, 'message': f'Archivo {consolidated_file_path} subido con éxito'}

    except Exception as e:
        print(f"Error al subir el archivo {consolidated_file_path} a Cloud Storage: {e}")
        return {'success': False, 'message': f"Error al subir el archivo {consolidated_file_path} a Cloud Storage: {e}"}

# Función para descargar el archivo JSON existente, agregarle los nuevos datos y volver a subirlo
def update_on_gcs_consolidated_json(new_data, consolidated_file_path):
    print("update_consolidated_json")
    try:
        # 1. Descargar el archivo JSON existente desde Cloud Storage
        current_data = download_docs_embeddings_from_gcs(consolidated_file_path)

        # Si no se pudo descargar el archivo o está vacío, inicializamos con un array vacío
        if not current_data:
            current_data = []

        # 2. Actualizar el archivo con los nuevos datos
        current_data.append(new_data)

        # 3. Subir el archivo actualizado nuevamente a Cloud Storage
        upload_consolidate_embeddings_to_gcs(consolidated_file_path, current_data)

        return {'success': True, 'message': 'JSON consolidado actualizado con éxito'}
    
    except Exception as e:
        print(f"Error al actualizar el archivo JSON consolidado: {e}")
        return {'success': False, 'message': f"Error al actualizar el archivo JSON consolidado: {e}"}

# Extrae las URLs de los archivos .json en las carpetas de un path en Cloud Storage. - sin uso
def extract_data_from_json_products_embeddings(docs_path):
    """Recorre recursivamente las subcarpetas del path en Cloud Storage y extrae el contenido de los archivos .json.
    
    Args:
        docs_path (str): El path dentro del bucket donde se buscarán los archivos .json.

    Returns:
        list: Una lista de diccionarios que contienen la data combinada de todos los archivos .json.
    """

    print("extract_data_from_json_products_embeddings")
    try:
        # Inicializar cliente de Google Cloud Storage
        client = storage.Client()
        bucket = client.bucket()  # Cambiar 'your-bucket-name' por el nombre real de tu bucket

        # Obtener todos los blobs que están en el path de docs_sellers (recursivamente en subcarpetas)
        blobs = bucket.list_blobs(prefix=docs_path)

        # Inicializar la lista para almacenar la data combinada
        combined_data = []

        # Iterar sobre los blobs y filtrar aquellos que terminen en .json, incluso en subcarpetas
        for blob in blobs:
            if blob.name.endswith('.json'):
                # Descargar el contenido del archivo .json como una cadena de texto
                json_string = blob.download_as_text()

                # Parsear el contenido del JSON y añadirlo a la lista combinada
                json_data = json.loads(json_string)
                combined_data.append(json_data)

        return combined_data

    except Exception as e:
        print(f"Error al extraer y combinar data de los archivos .json: {e}")
        return []

# BUYERS