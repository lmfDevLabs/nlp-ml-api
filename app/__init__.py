from flask import Flask
from config import configure_app

def create_app():
    app = Flask(__name__)
    configure_app(app)

    from .routes import main_bp
    app.register_blueprint(main_bp)

    return app

