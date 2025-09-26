import httpx
import json
import re

EXTERNAL_API_URL = "https://score.hsborges.dev/api/score"

def fetch_score_data(params: dict, headers: dict):
    if 'cpf' in params:
        params['cpf'] = re.sub(r'[^\d]', '', params['cpf'])

    print(f"📡 Fazendo requisição para API externa com parâmetros: {params} e headers: {headers}...")
    try:
        with httpx.Client(timeout=10.0, headers=headers) as client:
            response = client.get(EXTERNAL_API_URL, params=params)
            response.raise_for_status()
            return response.json()
    except (httpx.RequestError, httpx.HTTPStatusError, json.JSONDecodeError) as exc:
        print(f"❌ Erro na chamada da API externa: {exc}")
        return None