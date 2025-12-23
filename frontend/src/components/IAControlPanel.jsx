import { useState } from 'react';

const IAControlPanel = () => {
  const [loadingTrain, setLoadingTrain] = useState(false);
  
  const [searchId, setSearchId] = useState('');
  const [prediccion, setPrediccion] = useState(null);
  const [loadingPredict, setLoadingPredict] = useState(false);
  const [error, setError] = useState(null);

  // 1. ENTRENAR (POST /ml/entrenar)
  const handleTrain = async () => {
    setLoadingTrain(true);
    try {
      // URL ACTUALIZADA SEGÚN TU ROUTER
      const res = await fetch('http://127.0.0.1:8000/ml/entrenar', { method: 'POST' });
      if (!res.ok) throw new Error('Error en entrenamiento');
      
      const data = await res.json();
      alert(`✅ ${data.message || "Modelo entrenado correctamente"}`);
    } catch (err) {
      alert("❌ Error: No se pudo entrenar el modelo.");
    } finally {
      setLoadingTrain(false);
    }
  };

  // 2. PREDECIR (GET /usuarios/{id}/perfil-ia)
  const handlePredict = async (e) => {
    e.preventDefault();
    if (!searchId) return;

    setLoadingPredict(true);
    setError(null);
    setPrediccion(null);

    try {
      // URL ACTUALIZADA SEGÚN TU ROUTER
      const res = await fetch(`http://127.0.0.1:8000/usuarios/${searchId}/perfil-ia`);
      const data = await res.json();

      if (!res.ok) throw new Error(data.detail || 'Error al obtener perfil');
      setPrediccion(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoadingPredict(false);
    }
  };

  return (
    <div className="bg-white rounded-2xl shadow-xl border border-indigo-100 overflow-hidden mb-10">
      
      {/* CABECERA */}
      <div className="bg-gradient-to-r from-violet-600 to-indigo-600 p-6 text-white">
        <h2 className="text-2xl font-black flex items-center gap-2">
          🧠 Centro de Control IA
        </h2>
        <p className="text-indigo-100 opacity-80 text-sm">Entrena el modelo y consulta perfiles en tiempo real</p>
      </div>

      <div className="p-6 grid grid-cols-1 md:grid-cols-2 gap-8">
        
        {/* COLUMNA IZQUIERDA: ENTRENAMIENTO */}
        <div className="border-b md:border-b-0 md:border-r border-gray-100 pb-6 md:pb-0 md:pr-6">
          <h3 className="font-bold text-gray-700 mb-2">🔄 Re-entrenamiento</h3>
          <p className="text-sm text-gray-400 mb-4">
            Actualiza el algoritmo con los últimos registros de todos los usuarios.
          </p>
          <button
            onClick={handleTrain}
            disabled={loadingTrain}
            className={`w-full py-3 rounded-xl font-bold text-white shadow-lg transition-transform active:scale-95 flex justify-center items-center gap-2
              ${loadingTrain ? 'bg-gray-400 cursor-not-allowed' : 'bg-black hover:bg-gray-800'}`}
          >
            {loadingTrain ? 'Entrenando...' : '🧠 ENTRENAR AHORA'}
          </button>
        </div>

        {/* COLUMNA DERECHA: CONSULTA */}
        <div>
          <h3 className="font-bold text-gray-700 mb-2">🔍 Consultar Perfil</h3>
          <form onSubmit={handlePredict} className="flex gap-2 mb-4">
            <input 
              type="number" 
              placeholder="ID Usuario (Ej: 1)" 
              value={searchId}
              onChange={(e) => setSearchId(e.target.value)}
              className="flex-1 border-2 border-gray-200 rounded-lg p-2 focus:border-indigo-500 outline-none"
            />
            <button 
              type="submit"
              disabled={loadingPredict}
              className="bg-indigo-600 text-white px-4 rounded-lg font-bold hover:bg-indigo-700 disabled:bg-indigo-300"
            >
              {loadingPredict ? '...' : 'Buscar'}
            </button>
          </form>

          {/* RESULTADOS */}
          {error && <p className="text-red-500 text-sm font-bold bg-red-50 p-2 rounded">⚠️ {error}</p>}
          
          {prediccion && (
            <div className="bg-indigo-50 rounded-xl p-4 border border-indigo-100 animate-fade-in">
              <div className="flex justify-between items-center mb-2">
                <span className="text-xs font-bold text-indigo-400 uppercase">Perfil Detectado</span>
                <span className="bg-indigo-600 text-white text-xs px-2 py-1 rounded-full font-bold">GRUPO {prediccion.grupo_id}</span>
              </div>
              <h4 className="text-2xl font-black text-indigo-900 mb-2">{prediccion.perfil_ia}</h4>
              <p className="text-sm text-gray-600 italic">"{prediccion.recomendacion}"</p>
              
              {/* Métricas clave (opcional) */}
              <div className="mt-3 grid grid-cols-2 gap-2 text-xs text-gray-500 border-t pt-2">
                 <span>IMC: {prediccion.metricas?.imc}</span>
                 <span>Edad: {prediccion.metricas?.edad}</span>
              </div>
            </div>
          )}
        </div>

      </div>
    </div>
  );
};

export default IAControlPanel;