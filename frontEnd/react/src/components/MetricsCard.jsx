import { useState, useEffect } from 'react';
import { LineChart, Activity, Server, CheckCircle, AlertCircle, XCircle } from 'lucide-react';
import { getDashboardMetrics } from '../api/services/formServices';

// Componente para um item individual da métrica, para não repetir código
const MetricItem = ({ icon: Icon, label, value, color }) => (
  <div className="flex items-center justify-between p-3 bg-gray-900/50 rounded-lg">
    <div className="flex items-center">
      <Icon className={`w-5 h-5 ${color}`} />
      <span className="ml-3 text-gray-300">{label}</span>
    </div>
    <span className={`font-bold text-lg ${color}`}>{value}</span>
  </div>
);

const MetricsCard = () => {
  const [metrics, setMetrics] = useState({
    requests_total: 0,
    requests_successful_total: 0,
    requests_failed_total: 0,
    requests_dropped_total: 0,
    queue_size_current: 0,
  });
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchMetrics = async () => {
      try {
        const data = await getDashboardMetrics();
        setMetrics(data);
        setError(null);
      } catch (err) {
        setError('Falha ao carregar métricas.');
        console.error(err);
      }
    };

    fetchMetrics(); // Busca na primeira vez
    const intervalId = setInterval(fetchMetrics, 2000); // E depois a cada 2 segundos

    return () => clearInterval(intervalId); // Limpa o intervalo quando o componente é desmontado
  }, []);

  return (
    <div className="bg-black border-2 border-green-600 rounded-xl shadow-2xl p-6 sm:p-8">
      <div className="flex items-center mb-6">
        <LineChart className="w-8 h-8 text-green-400" />
        <h2 className="text-2xl font-bold text-green-400 ml-3">Métricas em Tempo Real</h2>
      </div>
      
      {error ? (
        <div className="text-red-400 text-center">{error}</div>
      ) : (
        <div className="space-y-3">
          <MetricItem icon={Activity} label="Total de Requisições" value={metrics.requests_total} color="text-blue-400" />
          <MetricItem icon={Server} label="Itens na Fila" value={metrics.queue_size_current} color="text-yellow-400" />
          <MetricItem icon={CheckCircle} label="Sucessos" value={metrics.requests_successful_total} color="text-green-400" />
          <MetricItem icon={AlertCircle} label="Falhas" value={metrics.requests_failed_total} color="text-red-400" />
          <MetricItem icon={XCircle} label="Descartadas (Fila Cheia)" value={metrics.requests_dropped_total} color="text-orange-400" />
        </div>
      )}
    </div>
  );
};

export default MetricsCard;