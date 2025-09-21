import apiClient from './apiClient'; // Corrija o nome do arquivo se necessário

export const getScore = (cpf, clientId) => {
  return apiClient('/proxy/score', {
    params: { cpf },
    headers: { 'client-id': clientId },
  });
};

export const checkHealth = () => {
  return apiClient('/health');
};

// --- NOVA FUNÇÃO ---
export const getDashboardMetrics = () => {
  return apiClient('/dashboard-metrics');
};