from flask import Blueprint, jsonify, request
import queue
from concurrent.futures import Future

from ..core.queue_worker import REQUEST_QUEUE
from ..core.command import ScoreRequestCommand
from ..utils import metrics # Importa nossas métricas

api_bp = Blueprint('api', __name__)

@api_bp.route('/health')
def health_check():
    return jsonify({"status": "ok, serviço funcionando!"}), 200

@api_bp.route('/proxy/score')
def proxy_score():
    # Incrementa o total de requisições recebidas
    metrics.REQUESTS_TOTAL.inc()

    cpf = request.args.get('cpf')
    client_id = request.headers.get('client-id') or request.args.get('client-id')

    if not cpf:
        return jsonify({"error": "Parâmetro 'cpf' é obrigatório."}), 400
    if not client_id:
        return jsonify({"error": "Header ou parâmetro 'client-id' é obrigatório."}), 401

    request_params = {'cpf': cpf}
    request_headers = {'client-id': client_id}
    future = Future()
    command = ScoreRequestCommand(params=request_params, headers=request_headers, future=future)

    try:
        REQUEST_QUEUE.put_nowait(command)
        result = future.result(timeout=60)

        if result:
            return jsonify(result), 200
        else:
            return jsonify({"error": "Falha ao processar a requisição no serviço externo."}), 502

    except queue.Full:
        # Incrementa o total de requisições descartadas
        metrics.REQUESTS_DROPPED_TOTAL.inc()
        return jsonify({"error": "Serviço ocupado, a fila está cheia."}), 503
    except Exception as e:
        return jsonify({"error": f"Ocorreu um erro no processamento: {str(e)}"}), 500

@api_bp.route('/dashboard-metrics')
def get_dashboard_metrics():
    """Retorna as métricas atuais em um formato JSON para o frontend."""
    # Acessamos o valor interno dos contadores para enviar via JSON
    data = {
        'requests_total': int(metrics.REQUESTS_TOTAL._value.get()),
        'requests_successful_total': int(metrics.REQUESTS_SUCCESSFUL_TOTAL._value.get()),
        'requests_failed_total': int(metrics.REQUESTS_FAILED_TOTAL._value.get()),
        'requests_dropped_total': int(metrics.REQUESTS_DROPPED_TOTAL._value.get()),
        'queue_size_current': int(metrics.QUEUE_SIZE._value.get()),
    }
    return jsonify(data)