from google.cloud import pubsub_v1
import os
from app.handlers.text_processing import preprocess_text
from app.handlers.vector_operations import vector_distance
from app.utilities.firestore_utils import load_embeddings_from_storage
from app.handlers.openai_embeddings import generate_openai_embeddings

def process_message(message):
    # Decodificar el mensaje de Pub/Sub
    message_data = message.data.decode('utf-8')
    print(f'Received message: {message_data}')
    
    # Aquí puedes agregar la lógica para procesar el mensaje
    # Preprocesar el texto
    #preprocessed_query = preprocess_text(message_data)
    
    # Generar embeddings para la consulta del usuario
    #user_embedding = generate_openai_embeddings(preprocessed_query)
    
    # Cargar embeddings desde Cloud Storage
    #embeddings_data = load_embeddings_from_storage(os.getenv('GCS_BUCKET_NAME'), 'path-to-your-embeddings-file.json')
    
    # Buscar en la base de datos vectorial
    #results = vector_distance(user_embedding, embeddings_data)
    
    #print(f'Processed results: {results}')
    
    # Acknowledge the message to remove it from the queue
    message.ack()

def start_consuming():
    print('Hi publisher')
    # Esto debería funcionar si las credenciales están configuradas correctamente
    publisher = pubsub_v1.PublisherClient()
    project_id = "sensebuy-e8add"
    topic_id = "chats"

    topic_path = publisher.topic_path(project_id, topic_id)

    try:
        future = publisher.publish(topic_path, b'Test message')
        print(f'Published message to {topic_path}: {future.result()}')
    except Exception as e:
        print(f'Error publishing message: {e}')
    # subscriber = pubsub_v1.SubscriberClient()
    # subscription_path = subscriber.subscription_path(os.getenv('GCP_PROJECT_ID'), os.getenv('GCP_TOPIC_SUSPCRIPTION_ID'))
    
    # streaming_pull_future = subscriber.subscribe(subscription_path, callback=process_message)
    # print(f'Listening for messages on {subscription_path}...')
    
    # try:
    #     streaming_pull_future.result()
    # except Exception as e:
    #     print(f"An error occurred: {e}")
    #     streaming_pull_future.cancel()

if __name__ == '__main__':
    start_consuming()