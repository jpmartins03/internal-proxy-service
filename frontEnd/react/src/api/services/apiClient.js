// frontEnd/react/src/api/services/apiClient.js

import { API_BASE_URL } from './apiConfig';

const apiClient = async (endpoint, options = {}) => {
  const { params, headers, ...customConfig } = options;

  let url = `${API_BASE_URL}${endpoint}`;

  if (params) {
    const queryParams = new URLSearchParams(params);
    url += `?${queryParams}`;
  }

  const config = {
    method: 'GET', // Default para GET
    headers: {
      'Content-Type': 'application/json',
      ...headers,
    },
    ...customConfig,
  };

  try {
    const response = await fetch(url, config);
    const data = await response.json();

    if (!response.ok) {
      // Se a resposta não for OK, joga um erro com a mensagem da API
      throw new Error(data.error || 'Ocorreu um erro na API.');
    }

    return data;
  } catch (error) {
    // Re-lança o erro para ser capturado no componente
    throw new Error(error.message || 'Falha na comunicação com o servidor.');
  }
};

export default apiClient;