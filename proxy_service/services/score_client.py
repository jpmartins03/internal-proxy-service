# proxy_service/services/score_client.py

import httpx
import json
import re # Importa a biblioteca de expressões regulares

# A URL correta, conforme a documentação do Swagger
EXTERNAL_API_URL = "https://score.hsborges.dev/api/score"

def fetch_score_data(params: dict, headers: dict):
    """
    Faz a requisição GET real para a API externa, incluindo os headers.
    """
    # Garante que estamos enviando apenas os números do CPF, removendo pontos e traços.
    if 'cpf' in params:
        params['cpf'] = re.sub(r'[^\d]', '', params['cpf'])

    print(f"📡 Fazendo requisição para API externa com parâmetros: {params} e headers: {headers}...")
    try:
        with httpx.Client(timeout=10.0, headers=headers) as client:
            response = client.get(EXTERNAL_API_URL, params=params)
            response.raise_for_status()

            print(f"✅ Resposta recebida da API externa: {response.status_code}")
            return response.json()

    except httpx.RequestError as exc:
        print(f"❌ Ocorreu um erro na requisição: {exc}")
        return None
    except httpx.HTTPStatusError as exc:
        print(f"❌ Erro de status HTTP: {exc.response.status_code} - {exc.response.text}")
        return None
    except json.JSONDecodeError:
        print(f"❌ Erro de decodificação: A API não retornou um JSON válido.")
        return None