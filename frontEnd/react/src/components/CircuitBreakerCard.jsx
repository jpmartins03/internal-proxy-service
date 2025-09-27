import { useState, useEffect } from 'react';
import { Zap, ZapOff, AlertTriangle } from 'lucide-react';
import { getCircuitBreakerStatus } from '../api/services/formServices';

const CircuitBreakerCard = () => {
  const [status, setStatus] = useState({ state: 'loading' });

  useEffect(() => {
    const fetchStatus = async () => {
      try {
        const data = await getCircuitBreakerStatus();
        setStatus(data);
      } catch (err) {
        setStatus({ state: 'error' });
        console.error(err);
      }
    };

    fetchStatus();
    const intervalId = setInterval(fetchStatus, 2000); // Atualiza a cada 2 segundos

    return () => clearInterval(intervalId); // Limpa o intervalo quando o componente é desmontado
  }, []);

  const stateInfo = {
    closed: { text: 'FECHADO', color: 'text-green-400', icon: <Zap /> },
    open: { text: 'ABERTO', color: 'text-red-400', icon: <ZapOff /> },
    half_open: { text: 'MEIO-ABERTO', color: 'text-yellow-400', icon: <AlertTriangle /> },
    loading: { text: 'A carregar...', color: 'text-gray-400', icon: null },
    error: { text: 'Erro ao buscar estado', color: 'text-red-500', icon: null },
  };

  const currentStatus = stateInfo[status.state] || stateInfo.error;

  return (
    <div className="bg-black border-2 border-green-600 rounded-xl shadow-2xl p-6 sm:p-8">
      <div className="flex items-center mb-4">
        {currentStatus.icon && <div className="mr-3">{currentStatus.icon}</div>}
        <h2 className="text-2xl font-bold text-green-400">Circuit Breaker</h2>
      </div>
      <div className="text-center bg-gray-900/50 p-4 rounded-lg">
        <p className="text-gray-400 text-sm mb-1">Estado Atual</p>
        <p className={`text-3xl font-bold ${currentStatus.color}`}>{currentStatus.text}</p>
        {status.state === 'closed' && (
          <p className="text-xs text-gray-500 mt-2">Falhas consecutivas: {status.failures} / {status.fail_max}</p>
        )}
      </div>
      <p className="text-xs text-gray-500 mt-4 text-center">
        O circuito abrirá após {status.fail_max || 3} falhas consecutivas, bloqueando novas chamadas por 30 segundos.
      </p>
    </div>
  );
};

export default CircuitBreakerCard;