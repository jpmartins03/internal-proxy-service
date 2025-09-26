from flask import Blueprint, jsonify, request
import queue
from concurrent.futures import Future
import itertools
import re
import time
import os

from ..core.queue_worker import REQUEST_QUEUE
from ..core.command import ScoreRequestCommand
from ..utils import metrics
from ..services.score_client import SCORE_CACHE, CACHE_TTL_SECONDS, api_breaker

api_bp = Blueprint('api', __name__)
request_counter = itertools.count()

# Lê o timeout da requisição do ambiente
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT_SECONDS", 60))

@api_bp.route('/health')
def health_check():
    return jsonify({"status": "ok, serviço funcionando!"}), 200

@api_bp.route('/proxy/score')
def proxy_score():
    metrics.REQUESTS_TOTAL.inc()
    cpf = request.args.get('cpf')
    client_id = request.headers.get('client-id') or request.args.get('client-id')
    priority = request.args.get('priority')

    current_strategy = "PRIORITY" if priority is not None else "FIFO"
    effective_priority = int(priority) if priority is not None else 10

    if not cpf or not client_id:
        return jsonify({"error": "Parâmetros/Headers faltando."}), 400
        
    tie_breaker = next(request_counter)
    print(f"📥 Recebida requisição #{tie_breaker} para CPF {cpf}. Modo: [{current_strategy}], Prioridade: [{effective_priority}].")
    request_params = {'cpf': cpf}
    request_headers = {'client-id': client_id}
    future = Future()
    command = ScoreRequestCommand(params=request_params, headers=request_headers, future=future)

    try:
        REQUEST_QUEUE.put_nowait(command, priority=effective_priority, tie_breaker=tie_breaker)
        # Usa o timeout lido do ambiente
        result = future.result(timeout=REQUEST_TIMEOUT)

        if result:
            return jsonify(result), 200
        else:
            return jsonify({"error": "Falha ao processar a requisição no serviço externo."}), 502

    except queue.Full:
        print("⚠️ Fila cheia! Tentando fallback para o cache...")
        cache_key = re.sub(r'[^\d]', '', cpf)
        current_time = time.time()
        
        if cache_key in SCORE_CACHE:
            cached_item = SCORE_CACHE[cache_key]
            if current_time - cached_item['timestamp'] < CACHE_TTL_SECONDS:
                print(f"✅ FALLBACK SUCCESS! Servindo resposta do cache para o CPF {cache_key}.")
                metrics.REQUESTS_SUCCESSFUL_TOTAL.inc()
                response = jsonify(cached_item['data'])
                response.headers['X-Proxy-Fallback'] = 'cache'
                return response, 200

        print(f"❌ FALLBACK FAILED. Descartando requisição.")
        metrics.REQUESTS_DROPPED_TOTAL.inc()
        return jsonify({"error": "Serviço ocupado, a fila está cheia e não há cache disponível."}), 503

    except Exception as e:
        metrics.REQUESTS_FAILED_TOTAL.inc()
        return jsonify({"error": f"Ocorreu um erro no processamento: {str(e)}"}), 500

@api_bp.route('/dashboard-metrics')
def get_dashboard_metrics():
    latency_count = metrics.REQUEST_LATENCY_COUNT._value.get()
    latency_sum = metrics.REQUEST_LATENCY_SUM._value.get()
    avg_latency = 0
    if latency_count > 0:
        avg_latency = latency_sum / latency_count
    data = {
        'requests_total': int(metrics.REQUESTS_TOTAL._value.get()),
        'requests_successful_total': int(metrics.REQUESTS_SUCCESSFUL_TOTAL._value.get()),
        'requests_failed_total': int(metrics.REQUESTS_FAILED_TOTAL._value.get()),
        'requests_dropped_total': int(metrics.REQUESTS_DROPPED_TOTAL._value.get()),
        'queue_size_current': int(metrics.QUEUE_SIZE._value.get()),
        'average_latency_seconds': round(avg_latency, 4)
    }
    return jsonify(data)

@api_bp.route('/circuit-breaker-status')
def get_circuit_breaker_status():
    return jsonify({
        "state": api_breaker.current_state,
        "failures": api_breaker.fail_counter,
        "fail_max": api_breaker.fail_max,
    })