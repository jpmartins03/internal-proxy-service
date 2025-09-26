from ..services.score_client import fetch_score_data
from ..utils import metrics

class ScoreRequestCommand:
    def __init__(self, params: dict, headers: dict, future):
        self.params = params
        self.headers = headers
        self.future = future

    def execute(self):
        print(f"Executando Command com parâmetros: {self.params}")
        response_data = fetch_score_data(self.params, self.headers)

        if response_data:
            metrics.REQUESTS_SUCCESSFUL_TOTAL.inc()
        else:
            metrics.REQUESTS_FAILED_TOTAL.inc()

        self.future.set_result(response_data)