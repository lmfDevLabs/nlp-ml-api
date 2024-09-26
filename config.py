import os
class Config:
    # Configuración básica de Flask
    DEBUG = True  # Cambiar a False en producción
    TESTING = False

    # Configuración de OpenAI
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    
    # Configuración de Google Cloud Storage
    GCP_PROJECT_ID = os.getenv('GCP_PROJECT_ID', 'sensebuy-e8add')
    GCS_BUCKET_NAME = os.getenv('GCS_BUCKET_NAME', 'your-bucket-name')
    GCP_TOPIC_SUSPCRIPTION_ID = os.getenv('GCP_TOPIC_SUSPCRIPTION_ID', 'chats-sub')

class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False

class TestingConfig(Config):
    DEBUG = False
    TESTING = True

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False

# configure_app
def configure_app(app):
    # Cargar la configuración en la aplicación Flask
    app.config.from_object(Config)

    # Configuraciones adicionales
    if app.config['DEBUG']:
        app.logger.setLevel('DEBUG')

