from flask import Flask
from flask_cors import CORS # Importa a biblioteca

def create_app():
    """
    Esta é a "Application Factory".
    Ela cria e configura a aplicação Flask.
    """
    app = Flask(__name__)

    # --- CONFIGURAÇÃO DO CORS ---
    # Esta linha permite que qualquer origem (*) acesse sua API.
    # É seguro para desenvolvimento.
    CORS(app)
    # --------------------------

    # Inicia o nosso worker em segundo plano
    from .core.queue_worker import start_worker
    start_worker()

    # Registra os endpoints da API
    from .api import routes
    app.register_blueprint(routes.api_bp)

    return app
