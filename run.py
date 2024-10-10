from flask import Flask
import firebase_admin
from firebase_admin import credentials 
# routes
from app.routes import main_bp  

def create_app():
    # Crear la app de Flask
    app = Flask(__name__)
    
    try:
        # Inicializar Firebase con credenciales de cuenta de servicio
        cred = credentials.Certificate("./gcp_service_accounts/sensebuy-e8add-c83b372813c1.json")
        # cred = credentials.Certificate("/app/service-account-file.json")
        default_app = firebase_admin.initialize_app(cred, {
            'storageBucket': 'sensebuy-e8add.appspot.com'
        })
        print(default_app.name)
        
    except Exception as e:
        print(f"Error al inicializar Firebase: {e}")
        # Aquí podrías detener la aplicación o manejar la excepción de otra manera
        raise e  # Opcional: para hacer que la app falle si Firebase no se inicializa

    # Otras configuraciones y rutas de la aplicación
    app.register_blueprint(main_bp)
    
    return app

# Crear la aplicación
app = create_app()

if __name__ == '__main__':
    # Ejecutar la aplicación en modo debug si FLASK_DEBUG está habilitado
    app.run(host="0.0.0.0", port=8080)