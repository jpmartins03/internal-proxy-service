# run.py

from proxy_service import create_app

# Cria a instância da nossa aplicação Flask usando a "fábrica"
app = create_app()

if __name__ == "__main__":
    # Este bloco só executa quando você roda 'python run.py'
    # Em produção, usaremos um servidor diferente (Gunicorn)
    print("🚀 Servidor do Proxy iniciando em http://127.0.0.1:5000")
    app.run(host="0.0.0.0", port=5000)