import { useState, useEffect } from 'react';
import { checkHealth } from '../api/services/formServices';
import { Wifi, Server, Activity, Power } from 'lucide-react';

const HealthCheckCard = () => {
  // Estados: 'checking', 'online', 'offline'
  const [status, setStatus] = useState('checking');
  const [lastChecked, setLastChecked] = useState(null);

  const performCheck = async () => {
    setStatus('checking');
    try {
      await checkHealth();
      setStatus('online');
    } catch (error) {
      setStatus('offline');
    }
    setLastChecked(new Date().toLocaleTimeString());
  };

  // Roda a verificação uma vez quando o componente é carregado
  useEffect(() => {
    performCheck();
  }, []);

  const statusInfo = {
    online: {
      color: 'text-green-400',
      bgColor: 'bg-green-500',
      text: 'Online',
      icon: <Wifi size={24} />,
    },
    offline: {
      color: 'text-red-400',
      bgColor: 'bg-red-500',
      text: 'Offline',
      icon: <Power size={24} />,
    },
    checking: {
      color: 'text-yellow-400',
      bgColor: 'bg-yellow-500',
      text: 'Verificando...',
      icon: <Activity size={24} />,
    },
  };

  const currentStatus = statusInfo[status];

  return (
    <div className="bg-black border-2 border-green-600 rounded-xl shadow-2xl p-6 sm:p-8 flex flex-col justify-between">
      <div>
        <div className="flex items-center space-x-3 mb-1">
          <Server size={28} className="text-green-400" />
          <h2 className="text-2xl font-bold text-green-400">Status do Backend</h2>
        </div>
        <p className="text-green-400 mb-6">Verifica a conexão com o servidor Flask.</p>

        <div className={`flex items-center space-x-4 p-4 rounded-lg bg-gray-900/50 border border-gray-700`}>
          <div className={`w-4 h-4 rounded-full ${currentStatus.bgColor} animate-pulse`}></div>
          <span className={`text-xl font-semibold ${currentStatus.color}`}>{currentStatus.text}</span>
          <div className="flex-grow text-right text-gray-500">
            {currentStatus.icon}
          </div>
        </div>
        {lastChecked && <p className="text-xs text-gray-500 mt-2">Última verificação: {lastChecked}</p>}
      </div>
      <button
        onClick={performCheck}
        disabled={status === 'checking'}
        className="w-full mt-6 px-4 py-2 font-semibold text-green-400 bg-green-200/10 rounded-md hover:bg-green-200/20 disabled:opacity-50"
      >
        Verificar Novamente
      </button>
    </div>
  );
};

export default HealthCheckCard;