import { useState } from 'react';
import { Server } from 'lucide-react';
import './App.css';
import HealthCheckCard from './components/HealthCheckCard';
import BulkRequestCard from './components/BulkRequestCard';
import MetricsCard from './components/MetricsCard';
import ManualRequestCard from './components/ManualRequestCard';
import StrategySelector from './components/StrategySelector';

function App() {
  const [strategy, setStrategy] = useState('FIFO');

  return (
    <div className="min-h-screen w-full bg-black text-gray-200 flex flex-col items-center p-4 sm:p-6 lg:p-8 space-y-8">
      <div className="w-full max-w-7xl flex items-center space-x-4">
        <Server size={48} className="text-green-400"/>
        <div>
          <h1 className="text-4xl font-bold text-green-400">Dashboard do Proxy Interno</h1>
          <p className="text-green-400/80 mt-1">Monitore e teste o serviço de proxy em tempo real.</p>
        </div>
      </div>
      <StrategySelector strategy={strategy} setStrategy={setStrategy} />
      <div className="w-full max-w-7xl grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div className="space-y-8">
          <ManualRequestCard strategy={strategy} />
          <BulkRequestCard strategy={strategy} />
        </div>
        <div className="space-y-8">
          <HealthCheckCard />
          <MetricsCard />
        </div>
      </div>
    </div>
  );
}

export default App;