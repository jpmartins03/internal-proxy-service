import requests
import time
import threading

# --- Configurações do Teste ---
BASE_URL = "http://localhost:5000"
VALID_CPF = "xxx.xxx.xxx-xx" # substituir por um cpf real, nao coloquei aqui por motivos de segurança descrito no documento do trabalho 
CLIENT_ID = "12345678"
HEADERS = {"client-id": CLIENT_ID}

# --- Funções Auxiliares ---
def print_header(title):
    print("\n" + "="*50)
    print(f"  {title}")
    print("="*50)

def print_result(name, success, message=""):
    status = "✅ SUCESSO" if success else "❌ FALHA"
    print(f"[{status}] Teste: {name}. {message}")

# --- Cenários de Teste ---

def test_health_check():
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print_result("Health Check", True, f"Resposta: {response.json()}")
        else:
            print_result("Health Check", False, f"Status inesperado: {response.status_code}")
    except requests.ConnectionError:
        print_result("Health Check", False, "Não foi possível conectar ao servidor.")
        return False
    return True

def test_single_request():
    print_header("Cenário 1: Teste de Requisição Única")
    params = {"cpf": VALID_CPF}
    try:
        response = requests.get(f"{BASE_URL}/proxy/score", params=params, headers=HEADERS)
        if response.status_code == 200 and "score" in response.json():
            print_result("Requisição Única", True, f"Score recebido: {response.json()['score']}")
        else:
            print_result("Requisição Única", False, f"Resposta inesperada: {response.status_code} - {response.text}")
    except Exception as e:
        print_result("Requisição Única", False, f"Erro: {e}")

def test_burst_and_queue():
    print_header("Cenário 2: Teste de Rajada e Fila")
    
    start_time = time.time()
    
    def send_request(i):
        params = {"cpf": f"111111111{i:02}"}
        requests.get(f"{BASE_URL}/proxy/score", params=params, headers=HEADERS, timeout=30)
        print(f"Resposta da requisição {i} recebida.")

    threads = []
    for i in range(10):
        thread = threading.Thread(target=send_request, args=(i,))
        threads.append(thread)
        thread.start()
        print(f"Requisição {i} enviada...")

    for thread in threads:
        thread.join()

    end_time = time.time()
    duration = end_time - start_time
    
    print(f"\nTempo total para 10 requisições: {duration:.2f} segundos.")
    if 9.5 < duration < 11.5:
        print_result("Rajada e Fila", True, "O tempo de processamento está correto (aprox. 10s), indicando que a fila e o rate limit funcionaram.")
    else:
        print_result("Rajada e Fila", False, f"O tempo de processamento ({duration:.2f}s) está fora do esperado.")

if __name__ == "__main__":
    print_header("INICIANDO TEST HARNESS")
    if test_health_check():
        test_single_request()
        test_burst_and_queue()
    print("\nFIM DO TEST HARNESS")