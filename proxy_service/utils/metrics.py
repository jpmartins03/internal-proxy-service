from prometheus_client import Counter, Gauge

# --- Métricas existentes, sem alteração ---
REQUESTS_TOTAL = Counter('proxy_requests_total', 'Total de requisições recebidas.')
REQUESTS_SUCCESSFUL_TOTAL = Counter('proxy_requests_successful_total', 'Total de requisições com sucesso.')
REQUESTS_FAILED_TOTAL = Counter('proxy_requests_failed_total', 'Total de requisições com falha.')
REQUESTS_DROPPED_TOTAL = Counter('proxy_requests_dropped_total', 'Total de requisições descartadas.')
QUEUE_SIZE = Gauge('proxy_queue_size_current', 'Tamanho atual da fila.')


# --- NOVAS MÉTRICAS PARA LATÊNCIA ---
# Em vez de um Histograma, usamos métricas que sabemos acessar.

# Um contador para o número de requisições cuja latência foi medida
REQUEST_LATENCY_COUNT = Counter(
    'proxy_request_latency_count',
    'Contagem de requisições para cálculo de latência.'
)
# Um medidor para a soma total de todas as latências
REQUEST_LATENCY_SUM = Gauge(
    'proxy_request_latency_sum_seconds',
    'Soma total das latências de requisição em segundos.'
)