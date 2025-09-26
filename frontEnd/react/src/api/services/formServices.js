import apiClient from './apiClient';

// A função agora aceita um parâmetro opcional 'priority'
export const getScore = (cpf, clientId, priority = null) => {
  const params = { cpf };
  
  // Adiciona a prioridade aos parâmetros da URL apenas se ela for fornecida
  if (priority !== null && priority !== '') {
    params.priority = priority;
  }

  return apiClient('/proxy/score', {
    params, // Envia os parâmetros atualizados
    headers: { 'client-id': clientId },
  });
};

export const checkHealth = () => {
  return apiClient('/health');
};

export const getDashboardMetrics = () => {
  return apiClient('/dashboard-metrics');
};