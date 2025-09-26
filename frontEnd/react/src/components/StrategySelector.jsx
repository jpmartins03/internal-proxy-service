import { SlidersHorizontal } from 'lucide-react';

const StrategySelector = ({ strategy, setStrategy }) => {
  const isPriority = strategy === 'PRIORITY';
  return (
    <div className="bg-black border-2 border-green-600 rounded-xl shadow-2xl p-6 sm:p-8 w-full max-w-7xl">
      <div className="flex items-center mb-4">
        <SlidersHorizontal size={28} className="text-green-400" />
        <h2 className="text-2xl font-bold text-green-400 ml-3">Estratégia da Fila</h2>
      </div>
      <div className="flex items-center space-x-4">
        <span className={`font-semibold transition-colors ${!isPriority ? 'text-green-400' : 'text-gray-500'}`}>FIFO</span>
        <button onClick={() => setStrategy(isPriority ? 'FIFO' : 'PRIORITY')} className={`relative inline-flex items-center h-6 rounded-full w-11 transition-colors duration-300 focus:outline-none ${isPriority ? 'bg-green-600' : 'bg-gray-700'}`}>
          <span className={`inline-block w-4 h-4 transform bg-white rounded-full transition-transform duration-300 ${isPriority ? 'translate-x-6' : 'translate-x-1'}`} />
        </button>
        <span className={`font-semibold transition-colors ${isPriority ? 'text-green-400' : 'text-gray-500'}`}>PRIORITY</span>
      </div>
      <p className="text-gray-400 mt-3 text-sm">
        {isPriority ? "Requisições com menor número de prioridade serão processadas primeiro." : "As requisições serão processadas na ordem em que chegam."}
      </p>
    </div>
  );
};
export default StrategySelector;