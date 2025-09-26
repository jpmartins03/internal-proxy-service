import { useState } from 'react';
import { getScore } from '../api/services/formServices';
import { UploadCloud, CheckCircle, XCircle, Loader, List, Repeat, FileText, ChevronDown } from 'lucide-react';

const ModeButton = ({ children, onClick, isActive }) => (
    <button type="button" onClick={onClick} className={`px-4 py-2 text-sm font-semibold rounded-md flex items-center space-x-2 transition-colors duration-200 ${isActive ? 'bg-green-200/20 text-green-300' : 'bg-gray-800/50 text-gray-400 hover:bg-gray-700/50'}`}>
        {children}
    </button>
);

const BulkRequestCard = ({ strategy }) => {
    const [mode, setMode] = useState('list');
    const [cpfListText, setCpfListText] = useState('');
    const [singleCpf, setSingleCpf] = useState('');
    const [quantity, setQuantity] = useState(10);
    const [file, setFile] = useState(null);
    const [priority, setPriority] = useState('10');
    const [clientId, setClientId] = useState('202319070734');
    const [results, setResults] = useState([]);
    const [isLoading, setIsLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setIsLoading(true);
        setResults([]);
        let cpfList = [];

        if (mode === 'list') {
            cpfList = cpfListText.split('\n').map(cpf => cpf.trim()).filter(Boolean);
        } else if (mode === 'repeat') {
            cpfList = Array.from({ length: quantity }, () => singleCpf.trim());
        } else if (mode === 'file' && file) {
            const fileContent = await file.text();
            cpfList = fileContent.split('\n').map(cpf => cpf.trim()).filter(Boolean);
        }

        const initialResults = cpfList.map((cpf, index) => ({ id: `${cpf}-${index}`, cpf, status: 'pending', isOpen: false }));
        setResults(initialResults);

        const currentPriority = strategy === 'PRIORITY' ? priority : null;
        
        // --- LÓGICA CORRIGIDA E DEFINITIVA ---
        // 1. Dispara todas as requisições em paralelo.
        // A função .map executa todas as chamadas getScore imediatamente.
        cpfList.forEach((cpf, index) => {
            getScore(cpf, clientId, currentPriority)
                .then(data => {
                    // Sucesso: atualiza o item específico na lista de resultados
                    setResults(prev => prev.map((r, i) => 
                        i === index ? { ...r, status: 'success', data } : r
                    ));
                })
                .catch(error => {
                    // Falha: atualiza o item específico com a mensagem de erro
                    setResults(prev => prev.map((r, i) => 
                        i === index ? { ...r, status: 'error', error: error.message } : r
                    ));
                });
        });

        // 2. O botão de loading é desativado imediatamente após o disparo,
        // pois não estamos mais esperando (await) que todas terminem aqui.
        setIsLoading(false);
        // --------------------------------------------------
    };

    const handleToggleResult = (id) => {
        setResults(prev => prev.map(r => r.id === id ? { ...r, isOpen: !r.isOpen } : r));
    };

    const ResultIcon = ({ status }) => {
        if (status === 'success') return <CheckCircle className="text-green-400" size={20} />;
        if (status === 'error') return <XCircle className="text-red-400" size={20} />;
        return <Loader className="text-yellow-400 animate-spin" size={20} />;
    };

    return (
        <div className="bg-black border-2 border-green-600 rounded-xl shadow-2xl p-6 sm:p-8 col-span-1 md:col-span-2">
            <div className="flex items-center space-x-3 mb-1">
                <UploadCloud size={28} className="text-green-400" />
                <h2 className="text-2xl font-bold text-green-400">Gerador de Rajadas</h2>
            </div>
            <p className="text-green-400 mb-6">Selecione um método para enfileirar múltiplas requisições.</p>
            <form onSubmit={handleSubmit} className="space-y-6">
                <div className="flex space-x-2 p-1 bg-gray-900/50 rounded-lg">
                    <ModeButton onClick={() => setMode('list')} isActive={mode === 'list'}><List size={16}/><span>Lista de CPFs</span></ModeButton>
                    <ModeButton onClick={() => setMode('repeat')} isActive={mode === 'repeat'}><Repeat size={16}/><span>Repetir CPF</span></ModeButton>
                    <ModeButton onClick={() => setMode('file')} isActive={mode === 'file'}><FileText size={16}/><span>Arquivo .txt</span></ModeButton>
                </div>
                {mode === 'list' && (
                    <div>
                        <label htmlFor="cpfs" className="block text-sm font-medium text-green-400">Lista de CPFs (um por linha)</label>
                        <textarea id="cpfs" rows={5} value={cpfListText} onChange={(e) => setCpfListText(e.target.value)} placeholder="000.000.000-00&#10;111.111.111-11&#10;..." required className="w-full mt-1 input-style" />
                    </div>
                )}
                {mode === 'repeat' && (
                    <div className="grid grid-cols-3 gap-4">
                        <div className="col-span-2">
                            <label htmlFor="singleCpf" className="block text-sm font-medium text-green-400">CPF para Repetir</label>
                            <input type="text" id="singleCpf" value={singleCpf} onChange={(e) => setSingleCpf(e.target.value)} placeholder="Apenas números" required className="w-full mt-1 input-style" />
                        </div>
                        <div>
                            <label htmlFor="quantity" className="block text-sm font-medium text-green-400">Quantidade</label>
                            <input type="number" id="quantity" value={quantity} onChange={(e) => setQuantity(Number(e.target.value))} min="1" max="100" required className="w-full mt-1 input-style" />
                        </div>
                    </div>
                )}
                {mode === 'file' && (
                    <div>
                        <label htmlFor="file" className="block text-sm font-medium text-green-400">Arquivo de CPFs (.txt)</label>
                        <input type="file" id="file" onChange={(e) => setFile(e.target.files[0])} accept=".txt" required className="w-full mt-1 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-green-200/10 file:text-green-300 hover:file:bg-green-200/20 text-gray-400" />
                    </div>
                )}
                {strategy === 'PRIORITY' && (
                    <div>
                        <label htmlFor="bulk-priority" className="block text-sm font-medium text-green-400">Prioridade para a Rajada</label>
                        <input id="bulk-priority" type="number" value={priority} onChange={(e) => setPriority(e.target.value)} className="input-style" placeholder="Ex: 1 (alta), 10 (baixa)" />
                    </div>
                )}
                <div>
                    <label htmlFor="bulkClientId" className="block text-sm font-medium text-green-400">Client ID</label>
                    <input type="text" id="bulkClientId" value={clientId} onChange={(e) => setClientId(e.target.value)} required className="w-full mt-1 input-style" />
                </div>
                <button type="submit" disabled={isLoading} className="w-full px-4 py-2 font-semibold text-green-400 bg-green-200/10 rounded-md hover:bg-green-200/20 disabled:opacity-50 flex items-center justify-center">
                    {isLoading ? <div className="spinner"></div> : 'Enfileirar Todas as Requisições'}
                </button>
            </form>
            {results.length > 0 && (
                <div className="mt-6">
                    <h3 className="text-lg font-semibold text-green-300">Progresso das Requisições</h3>
                    <ul className="mt-2 space-y-2 max-h-60 overflow-y-auto pr-2">
                        {results.map((result) => (
                            <li key={result.id} className="bg-gray-900/50 rounded-md transition-all duration-300">
                                <button type="button" onClick={() => handleToggleResult(result.id)} disabled={result.status === 'pending'} className="w-full flex items-center justify-between text-sm p-2 text-left disabled:cursor-not-allowed">
                                    <span className="font-mono text-green-300">{result.cpf}</span>
                                    <div className="flex items-center space-x-2">
                                        <ResultIcon status={result.status} />
                                        {result.status !== 'pending' && (<ChevronDown className={`text-gray-400 transition-transform duration-200 ${result.isOpen ? 'rotate-180' : ''}`} size={16} />)}
                                    </div>
                                </button>
                                {result.isOpen && (
                                    <div className="p-2 border-t border-green-600/20">
                                        {result.status === 'success' && (<pre className="text-xs text-green-200 bg-black p-2 rounded overflow-auto">{JSON.stringify(result.data, null, 2)}</pre>)}
                                        {result.status === 'error' && (<p className="text-xs text-red-300">{result.error}</p>)}
                                    </div>
                                )}
                            </li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
};
export default BulkRequestCard;

