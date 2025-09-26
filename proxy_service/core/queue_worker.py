import os
import threading
import time
# Agora só precisamos da PriorityStrategy, pois ela cobre o caso FIFO
from .strategies import PriorityStrategy
from ..utils import metrics

# A fila agora é SEMPRE de prioridade. Isso simplifica o código e dá o controle ao frontend.
QUEUE_MAX_SIZE = int(os.getenv("QUEUE_MAX_SIZE", 100))
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
                command.future.set_exception(e)
        finally:
            REQUEST_QUEUE.task_done()
            metrics.QUEUE_SIZE.set(REQUEST_QUEUE.qsize())
            time.sleep(1)

def start_worker():
    print("Iniciando a thread do worker...")
    worker_thread = threading.Thread(target=worker_loop)
    worker_thread.daemon = True
    worker_thread.start()