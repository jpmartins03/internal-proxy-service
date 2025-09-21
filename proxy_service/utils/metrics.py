from prometheus_client import Counter, Gauge

# --- COUNTERS (Contadores que só aumentam) ---

# Total de requisições que chegam na nossa API
REQUESTS_TOTAL = Counter(
    'proxy_requests_total',
    'Total de requisições recebidas pelo proxy.'
)

# Total de requisições que o worker processou com sucesso
REQUESTS_SUCCESSFUL_TOTAL = Counter(
    'proxy_requests_successful_total',
    'Total de requisições processadas com sucesso (resposta da API externa OK).'
)

# Total de requisições que falharam (erro na API externa)
REQUESTS_FAILED_TOTAL = Counter(
    'proxy_requests_failed_total',
    'Total de requisições que falharam durante o processamento.'
)

# Total de requisições que foram recusadas por fila cheia
REQUESTS_DROPPED_TOTAL = Counter(
    'proxy_requests_dropped_total',
    'Total de requisições descartadas por a fila estar cheia.'
)


# --- GAUGES (Medidores que podem aumentar ou diminuir) ---

# Tamanho atual da fila
QUEUE_SIZE = Gauge(
    'proxy_queue_size_current',
    'Número atual de itens na fila de requisições.'
)