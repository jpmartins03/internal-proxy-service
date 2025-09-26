from flask import Flask
from flask_cors import CORS

def create_app():
    
    #configuação da aplicação do flask
    app = Flask(__name__)

    # CONFIGURAÇÃO DO CORS
    # ---------------------------------------------------------------------------------------------
    # Esta linha permite que qualquer origem (*) acesse a API.
    # É seguro para desenvolvimento.
    CORS(app)
    # ---------------------------------------------------------------------------------------------

    # essa função inicia o crador de threads em segundo plano que vai ficar "ouvindo" se uma requisi
    #ção chega na fila
    from .core.queue_worker import start_worker
    start_worker()

    # Registra os endpoints da API
    from .api import routes
    app.register_blueprint(routes.api_bp)

    return app
