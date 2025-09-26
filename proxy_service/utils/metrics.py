from prometheus_client import Counter, Gauge

REQUESTS_TOTAL = Counter('proxy_requests_total', 'Total de requisições recebidas.')
REQUESTS_SUCCESSFUL_TOTAL = Counter('proxy_requests_successful_total', 'Total de requisições com sucesso.')
REQUESTS_FAILED_TOTAL = Counter('proxy_requests_failed_total', 'Total de requisições com falha.')
REQUESTS_DROPPED_TOTAL = Counter('proxy_requests_dropped_total', 'Total de requisições descartadas.')
QUEUE_SIZE = Gauge('proxy_queue_size_current', 'Tamanho atual da fila.')