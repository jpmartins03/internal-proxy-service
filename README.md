# ***A documentação em pt-br esta no final desse arquivo***

# **Resilient Internal Proxy Challenge**

This project is a complete solution to the challenge of creating a resilient internal proxy service. It is designed to manage access to an external API with a strict rate limit (1 req/s), ensuring stability and observability even under load spikes.

The solution consists of two main parts:

1. **Backend (Python/Flask):** The proxy service itself, responsible for all the logic of queuing, rate limiting, caching, circuit breaking, and metrics.  
2. **Frontend (React/Vite/TailwindCSS):** A control and monitoring dashboard that allows interaction with the proxy, triggering load tests, and viewing the system's state in real-time.

## **🏛️ Architecture**

The system follows a decoupled architecture using the **Producer-Consumer** pattern:

* **Producers (Web Server Threads):** The Flask server receives HTTP requests from clients, encapsulates them into **Command** objects, and places them in a centralized queue.  
* **Consumer (Worker Thread):** A single **Worker** thread, running in the background, consumes commands from the queue at a controlled rate of **1 per second**.  
* **Buffer:** An in-memory priority queue acts as a buffer, absorbing bursts of requests and applying backpressure when its maximum capacity is reached.

## **🏗️ Design Patterns Used**
* Proxy: The central standard that defines the purpose of the service. 
* Command: Uncouples the request from its execution, allowing queuing. 
* Producer-Consumer: Models the flow of requests (Flask) to the processor (Worker). 
* Strategy: Allows dynamic selection of queuing policy (FIFO vs. Priority). 
* Circuit Breaker: Increases system resilience against external service failures. 
* Singleton (in fact): Ensures a single queue and worker instance for the entire application. 
* Application Factory: Organizes the creation of the Flask application

## **✨ Implemented Features**

The project meets all mandatory and most important optional requirements of the challenge:

* ✅ **Internal Queue/Buffer:** A queue with a maximum capacity to handle request spikes.  
* ✅ **Rate Limiter (Scheduler):** Ensures a maximum of 1 call per second to the upstream API.  
* ✅ **Caching with TTL:** Stores recent results in memory to avoid repeated calls and respond faster.  
* ✅ **Configurable Queueing Policy:** The frontend dynamically controls whether the queue behaves as FIFO or Priority.  
* ✅ **Degradation Strategy (Fallback):** If the queue is full, the system attempts to respond with cached data before dropping the request.  
* ✅ **Circuit Breaker:** Monitors failures from the external API and opens the circuit to prevent cascading failures.  
* ✅ **Complete Observability:** A comprehensive dashboard displays real-time metrics (Total requests, successes, failures, items in queue, average latency), backend status, and Circuit Breaker state.  
* ✅ **Configuration via .env:** Critical parameters like queue size, cache TTL, and timeouts are fully configurable.

## **🚀 How to Run**

The project requires two servers running simultaneously. You will need two terminals.

### **1\. Backend (Python/Flask Server)**

The backend is responsible for the proxy logic.

**Prerequisites:**

* Python 3.8+

Step 1: Install dependencies  
Navigate to the project root and install the required libraries:  
pip install \-r requirements.txt

Step 2: Configure the Environment  
Create a file named .env in the project root and add the following content. This file controls the proxy's behavior.  
\# Maximum request queue size  
QUEUE\_MAX\_SIZE=100

\# Cache item Time-To-Live (in seconds)  
CACHE\_TTL\_SECONDS=60

\# Timeout for the external API call (in seconds)  
EXTERNAL\_API\_TIMEOUT=10

\# Timeout for waiting for a request in the queue (in seconds)  
REQUEST\_TIMEOUT\_SECONDS=60

\# Worker's rate limiter delay (in seconds)  
RATE\_LIMIT\_SECONDS=1.0

\# Circuit Breaker settings  
CIRCUIT\_BREAKER\_FAIL\_MAX=3  
CIRCUIT\_BREAKER\_RESET\_TIMEOUT=30

Step 3: Start the Server  
In the project root, run:  
python3 run.py

The backend server will be running at http://localhost:5000.

### **2\. Frontend (React Dashboard)**

The frontend is the control and monitoring interface.

**Prerequisites:**

* Node.js and npm

Step 1: Install dependencies  
Navigate to the frontend folder and install the libraries:  
cd frontEnd/react  
npm install

Step 2: Start the Development Server  
Still in the frontEnd/react folder, run:  
npm run dev

The interface will be accessible at http://localhost:5173 (or another port indicated by Vite).

## **🧪 Testing the API Directly**

You can test the proxy endpoint directly via curl:

\# FIFO request (no priority)  
curl \-X GET 'http://localhost:5000/proxy/score?cpf=YOUR\_VALID\_CPF' \-H 'client-id: YOUR\_CLIENT\_ID'

\# High-priority request  
curl \-X GET 'http://localhost:5000/proxy/score?cpf=YOUR\_VALID\_CPF\&priority=1' \-H 'client-id: YOUR\_CLIENT\_ID'  


# **PT-BR**

# **Desafio Proxy Interno Resiliente**

Este projeto é uma solução completa para o desafio de criar um serviço de proxy interno resiliente. Ele foi projetado para gerenciar o acesso a uma API externa com um limite de taxa estrito (1 req/s), garantindo estabilidade e observabilidade mesmo sob picos de carga.

A solução é composta por duas partes principais:

1. **Backend (Python/Flask):** O serviço de proxy em si, responsável por toda a lógica de enfileiramento, rate limiting, cache, circuit breaker e métricas.  
2. **Frontend (React/Vite/TailwindCSS):** Um dashboard de controle e monitoramento que permite interagir com o proxy, disparar testes de carga e visualizar o estado do sistema em tempo real.

## **🏛️ Arquitetura**

O sistema segue uma arquitetura desacoplada utilizando o padrão **Produtor-Consumidor**:

* **Produtores (Web Server Threads):** O servidor Flask recebe as requisições HTTP dos clientes, as encapsula em objetos **Command** e as coloca em uma fila.  
* **Consumidor (Worker Thread):** Uma única thread **Worker**, rodando em segundo plano, consome os comandos da fila em um ritmo controlado de **1 por segundo**.  
* **Buffer:** Uma fila de prioridade em memória atua como um buffer, absorvendo rajadas de requisições e aplicando *backpressure* quando sua capacidade máxima é atingida.

## **🏗️ Padrões de Projeto Utilizados**
* Proxy: O padrão central que define o propósito do serviço.

* Command: Desacopla a requisição da sua execução, permitindo o enfileiramento.

* Producer-Consumer: Modela o fluxo de requisições (Flask) para o processador (Worker).

* Strategy: Permite a seleção dinâmica da política de enfileiramento (FIFO vs. Prioridade).

* Circuit Breaker: Aumenta a resiliência do sistema contra falhas do serviço externo.

* Singleton (de facto): Garante uma única instância da fila e do worker para toda a aplicação.

* Application Factory: Organiza a criação da aplicação Flask

## **✨ Funcionalidades Implementadas**

O projeto atende a todos os requisitos obrigatórios e opcionais mais importantes do desafio:

* ✅ **Fila/Buffer Interno:** Uma fila com capacidade máxima para lidar com picos de requisições.  
* ✅ **Rate Limiter (Scheduler):** Garante um máximo de 1 chamada por segundo para a API externa.  
* ✅ **Caching com TTL:** Armazena resultados recentes em memória para evitar chamadas repetidas.  
* ✅ **Política de Fila Configurável:** O frontend controla dinamicamente se a fila se comporta como FIFO ou Prioridade.  
* ✅ **Estratégia de Degradação (Fallback):** Se a fila está cheia, o sistema tenta responder com dados do cache antes de descartar a requisição.  
* ✅ **Circuit Breaker (Disjuntor):** Monitora falhas da API externa e abre o circuito para prevenir falhas em cascata.  
* ✅ **Observabilidade Completa:** Um dashboard completo exibe métricas em tempo real (Total de requisições, sucessos, falhas, itens na fila, latência média), status do backend e estado do Circuit Breaker.  
* ✅ **Configuração via .env:** Parâmetros críticos como tamanho da fila, TTL do cache e timeouts são totalmente configuráveis.

## **🚀 Como Executar**

O projeto requer dois servidores rodando simultaneamente. Você precisará de dois terminais.

### **1\. Backend (Servidor Python/Flask)**

O backend é responsável pela lógica do proxy.

**Pré-requisitos:**

* Python 3.8+

Passo 1: Instalar as dependências  
Navegue até a raiz do projeto e instale as bibliotecas necessárias:  
pip install \-r requirements.txt

Passo 2: Configurar o Ambiente  
Crie um arquivo chamado .env na raiz do projeto e adicione o seguinte conteúdo. Este arquivo controla o comportamento do proxy.  
\# Tamanho máximo da fila de requisições  
QUEUE\_MAX\_SIZE=100

\# Tempo de vida de um item no cache (em segundos)  
CACHE\_TTL\_SECONDS=60

\# Timeout para a chamada à API externa (em segundos)  
EXTERNAL\_API\_TIMEOUT=10

\# Timeout de espera para uma requisição na fila (em segundos)  
REQUEST\_TIMEOUT\_SECONDS=60

\# Atraso do Rate Limiter do worker (em segundos)  
RATE\_LIMIT\_SECONDS=1.0

\# Configurações do Circuit Breaker  
CIRCUIT\_BREAKER\_FAIL\_MAX=3  
CIRCUIT\_BREAKER\_RESET\_TIMEOUT=30

Passo 3: Iniciar o Servidor  
Na raiz do projeto, execute:  
python3 run.py

O servidor do backend estará rodando em http://localhost:5000.

### **2\. Frontend (Dashboard React)**

O frontend é a interface de controle e monitoramento.

**Pré-requisitos:**

* Node.js e npm

Passo 1: Instalar as dependências  
Navegue até a pasta do frontend e instale as bibliotecas:  
cd frontEnd/react  
npm install

Passo 2: Iniciar o Servidor de Desenvolvimento  
Ainda na pasta frontEnd/react, execute:  
npm run dev

A interface estará acessível em http://localhost:5173 (ou outra porta indicada pelo Vite).

## **🧪 Testando a API Diretamente**

Você pode testar o endpoint do proxy diretamente via curl:

\# Requisição FIFO (sem prioridade)  
curl \-X GET 'http://localhost:5000/proxy/score?cpf=SEU\_CPF\_VALIDO' \-H 'client-id: SEU\_CLIENT\_ID'

\# Requisição com alta prioridade  
curl \-X GET 'http://localhost:5000/proxy/score?cpf=SEU\_CPF\_VALIDO\&priority=1' \-H 'client-id: SEU\_CLIENT\_ID'  
