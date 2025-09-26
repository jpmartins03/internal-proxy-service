from flask import Blueprint, jsonify, request
import queue
from concurrent.futures import Future
import itertools # Importa a biblioteca para o contador

from ..core.queue_worker import REQUEST_QUEUE
from ..core.command import ScoreRequestCommand
from ..utils import metrics

api_bp = Blueprint('api', __name__)

# Um contador que gera um número único a cada chamada, de forma segura entre threads.
# Isto servirá como nosso critério de desempate.
request_counter = itertools.count()

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
        
    # Pega o próximo número do contador para usar como desempate
    tie_breaker = next(request_counter)

    print(f"📥 Recebida requisição #{tie_breaker} para CPF {cpf}. Modo: [{current_strategy}], Prioridade: [{effective_priority}].")

    request_params = {'cpf': cpf}
    request_headers = {'client-id': client_id}
    future = Future()
    command = ScoreRequestCommand(params=request_params, headers=request_headers, future=future)

    try:
        # Passa a prioridade E o critério de desempate para a fila
        REQUEST_QUEUE.put_nowait(command, priority=effective_priority, tie_breaker=tie_breaker)
        result = future.result(timeout=60)

        if result:
            return jsonify(result), 200
        else:
            return jsonify({"error": "Falha ao processar a requisição no serviço externo."}), 502

    except queue.Full:
        metrics.REQUESTS_DROPPED_TOTAL.inc()
        return jsonify({"error": "Serviço ocupado, a fila está cheia."}), 503
    except Exception as e:
        return jsonify({"error": f"Ocorreu um erro no processamento: {str(e)}"}), 500

@api_bp.route('/dashboard-metrics')
def get_dashboard_metrics():
    """Retorna as métricas atuais em um formato JSON para o frontend."""
    data = {
        'requests_total': int(metrics.REQUESTS_TOTAL._value.get()),
        'requests_successful_total': int(metrics.REQUESTS_SUCCESSFUL_TOTAL._value.get()),
        'requests_failed_total': int(metrics.REQUESTS_FAILED_TOTAL._value.get()),
        'requests_dropped_total': int(metrics.REQUESTS_DROPPED_TOTAL._value.get()),
        'queue_size_current': int(metrics.QUEUE_SIZE._value.get()),
    }
    return jsonify(data)