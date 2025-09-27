import os
import threading
import time
from .strategies import PriorityStrategy
from ..utils import metrics

QUEUE_MAX_SIZE = int(os.getenv("QUEUE_MAX_SIZE", 100))
# Lê o tempo de delay do rate limiter do ambiente
RATE_LIMIT_SECONDS = float(os.getenv("RATE_LIMIT_SECONDS", 1.0))
REQUEST_QUEUE = PriorityStrategy(maxsize=QUEUE_MAX_SIZE)

def worker_loop():
    print("🤖 Worker (Priority Queue) iniciado e aguardando tarefas na fila...")
    while True:
        metrics.QUEUE_SIZE.set(REQUEST_QUEUE.qsize())
        command = REQUEST_QUEUE.get()
        try:
            print(f"📥 Command recebido. Processando...")
            command.execute()
            print(f"✅ Command processado.")
        except Exception as e:
            print(f"🔥🔥🔥 ERRO CRÍTICO NO WORKER: {e}")
            if hasattr(command, 'future'):
                metrics.REQUESTS_FAILED_TOTAL.inc()
                command.future.set_exception(e)
        finally:
            REQUEST_QUEUE.task_done()
            metrics.QUEUE_SIZE.set(REQUEST_QUEUE.qsize())
            # Usa o delay lido do ambiente
            time.sleep(RATE_LIMIT_SECONDS)

def start_worker():
    print("Iniciando a thread do worker...")
    worker_thread = threading.Thread(target=worker_loop)
    worker_thread.daemon = True
    worker_thread.start()