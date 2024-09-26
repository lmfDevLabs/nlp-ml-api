import os
from app import create_app
from pubsub_consumer.pubsub_consumer import start_consuming

# Crear la aplicación
app = create_app()

if __name__ == '__main__':
    start_consuming()
    # Ejecutar la aplicación en modo debug si FLASK_DEBUG está habilitado
    app.run(debug=os.getenv('FLASK_DEBUG', False))