import { useState } from 'react';
import { getScore } from '../api/services/formServices';
import '../App.css'; // Para o spinner

const ManualRequestCard = () => {
    const [cpf, setCpf] = useState('');
    const [clientId, setClientId] = useState('202319070734');
    const [result, setResult] = useState(null);
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setResult(null);
        setError(null);

        try {
            const data = await getScore(cpf, clientId);
            setResult(data);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="bg-black border-2 border-green-600 rounded-xl shadow-2xl p-6 sm:p-8">
            <h2 className="text-2xl font-bold text-green-400 mb-1">Consulta Manual de Score</h2>
            <p className="text-green-400 mb-6">Digite os dados para uma consulta individual.</p>
            <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                    <label htmlFor="cpf" className="block text-sm font-medium text-green-400">CPF</label>
                    <input
                        type="text"
                        id="cpf"
                        value={cpf}
                        onChange={(e) => setCpf(e.target.value)}
                        placeholder="Apenas números"
                        required
                        className="w-full px-4 py-2 mt-1 bg-black text-green-400 border border-green-600 rounded-md focus:ring-green-500 focus:border-green-500"
                    />
                </div>
                <div>
                    <label htmlFor="clientId" className="block text-sm font-medium text-green-400">Client ID</label>
                    <input
                        type="text"
                        id="clientId"
                        value={clientId}
                        onChange={(e) => setClientId(e.target.value)}
                        required
                        className="w-full px-4 py-2 mt-1 bg-black text-green-400 border border-green-600 rounded-md focus:ring-green-500 focus:border-green-500"
                    />
                </div>
                <button
                    type="submit"
                    disabled={loading}
                    className="w-full px-4 py-2 font-semibold text-green-400 bg-green-200/10 rounded-md hover:bg-green-200/20 disabled:opacity-50 flex items-center justify-center"
                >
                    {loading ? <div className="spinner"></div> : 'Consultar'}
                </button>
            </form>

            {result && (
                <div className="mt-6 p-4 bg-green-900/50 border border-green-700 rounded-md">
                    <h3 className="text-lg font-semibold text-green-300">Resultado da Consulta</h3>
                    <pre className="mt-2 text-sm text-green-200 bg-gray-900 p-3 rounded overflow-auto">{JSON.stringify(result, null, 2)}</pre>
                </div>
            )}
            {error && (
                <div className="mt-6 p-4 bg-red-900/50 border border-red-700 rounded-md">
                    <h3 className="text-lg font-semibold text-red-300">Erro</h3>
                    <p className="mt-2 text-sm text-red-200">{error}</p>
                </div>
            )}
        </div>
    );
};

export default ManualRequestCard;