import httpx
import json
import re
import time
import os
from pybreaker import CircuitBreaker
from ..utils import metrics

# --- LÊ AS CONFIGURAÇÕES DO AMBIENTE ---
CACHE_TTL_SECONDS = int(os.getenv("CACHE_TTL_SECONDS", 60))
EXTERNAL_API_TIMEOUT = float(os.getenv("EXTERNAL_API_TIMEOUT", 10.0))
CB_FAIL_MAX = int(os.getenv("CIRCUIT_BREAKER_FAIL_MAX", 3))
CB_RESET_TIMEOUT = int(os.getenv("CIRCUIT_BREAKER_RESET_TIMEOUT", 30))
# ------------------------------------

SCORE_CACHE = {}
EXTERNAL_API_URL = "https://score.hsborges.dev/api/score"

# Configura o disjuntor com os valores do .env
api_breaker = CircuitBreaker(fail_max=CB_FAIL_MAX, reset_timeout=CB_RESET_TIMEOUT)

@api_breaker
def fetch_score_data(params: dict, headers: dict):
    """
    Busca os dados do score, utilizando o cache e o circuit breaker.
    """
    cpf_limpo = re.sub(r'[^\d]', '', params.get('cpf', ''))
    if not cpf_limpo:
        return None
    
    cache_key = cpf_limpo
    current_time = time.time()

    if cache_key in SCORE_CACHE:
        cached_item = SCORE_CACHE[cache_key]
        if current_time - cached_item['timestamp'] < CACHE_TTL_SECONDS:
            print(f"💾🎯 CACHE HIT! Retornando dados salvos para o CPF: {cache_key}")
            metrics.REQUEST_LATENCY_SUM.inc(0.001)
            metrics.REQUEST_LATENCY_COUNT.inc()
            return cached_item['data']

    print(f"💾❌ CACHE MISS. Buscando dados na API externa para o CPF: {cache_key}")
    api_params = {'cpf': cpf_limpo}

    start_time = time.time()
    try:
        print(f"📡 Fazendo requisição para API externa com parâmetros: {api_params} e headers: {headers}...")
        with httpx.Client(timeout=EXTERNAL_API_TIMEOUT, headers=headers) as client:
            response = client.get(EXTERNAL_API_URL, params=api_params)
            response.raise_for_status()
            response_data = response.json()
            SCORE_CACHE[cache_key] = {'data': response_data, 'timestamp': current_time}
            print(f"CACHE SET. Armazenando resultado para o CPF: {cache_key}")
            return response_data
    except (httpx.RequestError, httpx.HTTPStatusError, json.JSONDecodeError) as exc:
        print(f"❌ Erro na chamada da API externa: {exc}")
        raise exc
    finally:
        latency = time.time() - start_time
        metrics.REQUEST_LATENCY_SUM.inc(latency)
        metrics.REQUEST_LATENCY_COUNT.inc()
        print(f"⏱️ Latência da requisição: {latency:.4f} segundos")