import apiClient from './apiClient';

export const getScore = (cpf, clientId, priority = null) => {
  const params = { cpf };
  
  if (priority !== null && priority !== '') {
    params.priority = priority;
  }

  return apiClient('/proxy/score', {
    params,
    headers: { 'client-id': clientId },
  });
};

export const checkHealth = () => {
  return apiClient('/health');
};

export const getDashboardMetrics = () => {
  return apiClient('/dashboard-metrics');
};

// --- NOVA FUNÇÃO ADICIONADA ---
export const getCircuitBreakerStatus = () => {
  return apiClient('/circuit-breaker-status');
};