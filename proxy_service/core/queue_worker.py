import queue
import threading
import time
from ..utils import metrics # Importa nossas métricas

REQUEST_QUEUE = queue.Queue(maxsize=100)

def worker_loop():
    print("🤖 Worker iniciado e aguardando tarefas na fila...")
    while True:
        # Atualiza o medidor com o tamanho atual da fila ANTES de pegar um item
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
            # Garante que a tarefa seja marcada como concluída e a métrica da fila seja atualizada
            REQUEST_QUEUE.task_done()
            metrics.QUEUE_SIZE.set(REQUEST_QUEUE.qsize())
            time.sleep(1) # Mantém o rate limit

def start_worker():
    print("Iniciando a thread do worker...")
    worker_thread = threading.Thread(target=worker_loop)
    worker_thread.daemon = True
    worker_thread.start()