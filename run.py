from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env para o ambiente
load_dotenv()

from proxy_service import create_app

app = create_app()

if __name__ == "__main__":
    print("🚀 Servidor do Proxy iniciando em http://127.0.0.1:5000")
    app.run(host="0.0.0.0", port=5000)
