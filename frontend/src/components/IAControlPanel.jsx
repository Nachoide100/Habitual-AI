import { useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer, CartesianGrid } from 'recharts';

const IAControlPanel = () => {
  const [loadingTrain, setLoadingTrain] = useState(false);
  const [searchId, setSearchId] = useState('');
  const [prediccion, setPrediccion] = useState(null);
  const [loadingPredict, setLoadingPredict] = useState(false);
  const [error, setError] = useState(null);

  // 1. ENTRENAR
  const handleTrain = async () => {
    setLoadingTrain(true);
    try {
      const res = await fetch('http://127.0.0.1:8000/ml/entrenar', { method: 'POST' });
      if (!res.ok) throw new Error('Error en entrenamiento');
      const data = await res.json();
      alert(`✅ ${data.message || "Modelo entrenado"}`);
    } catch (err) {
      alert("❌ Error al entrenar.");
    } finally {
      setLoadingTrain(false);
    }
  };

  // 2. PREDECIR
  const handlePredict = async (e) => {
    e.preventDefault();
    if (!searchId) return;
    setLoadingPredict(true);
    setError(null);
    setPrediccion(null);

    try {
      // Petición al backend
      const res = await fetch(`http://127.0.0.1:8000/usuarios/${searchId}/perfil-ia`);
      const data = await res.json();

      if (!res.ok) throw new Error(data.detail || 'Error al obtener perfil');
      
      // --- CORRECCIÓN AQUÍ ---
      // 1. Definimos las claves que vamos a buscar
      const metricasClave = [
        { key: 'fitness_km', label: 'Fitness (Km)', color: '#10b981' },
        { key: 'ocio_digital_min', label: 'Pantalla (Min)', color: '#6366f1' },
        { key: 'lectura_paginas', label: 'Lectura (Pág)', color: '#06b6d4' },
        { key: 'vicios_score', label: 'Vicios (Puntos)', color: '#ef4444' },
        { key: 'sedentarismo_horas', label: 'Sentado (H)', color: '#f59e0b' }
      ];

      // 2. SEGURIDAD: Detectamos si el backend lo llama 'metricas_usuario' o 'metricas'
      // Si data.metricas_usuario existe, úsalo. Si no, busca data.metricas. Si no, usa objeto vacío {}.
      const misDatos = data.metricas_usuario || data.metricas || {}; 
      const datosGrupo = data.comparativa_grupo || {};

      // 3. Mapeamos los datos usando los objetos seguros "misDatos" y "datosGrupo"
      const datosGrafica = metricasClave.map(m => ({
        name: m.label,
        Tu: misDatos[m.key] || 0,     
        Media: datosGrupo[m.key] || 0  
      }));
      // -----------------------

      // Guardamos en el estado
      setPrediccion({ ...data, datosGrafica });

    } catch (err) {
      console.error(err); // Añadido para ver errores en consola (F12)
      setError(err.message);
    } finally {
      setLoadingPredict(false);
    }
    };
  return (
    <div className="bg-white rounded-2xl shadow-xl border border-indigo-100 overflow-hidden mb-10">
      
      <div className="bg-gradient-to-r from-violet-600 to-indigo-600 p-6 text-white">
        <h2 className="text-2xl font-black flex items-center gap-2">
          🧠 Centro de Control IA
        </h2>
        <p className="text-indigo-100 opacity-80 text-sm">Compara tus métricas con la media de tu tribu</p>
      </div>

      <div className="p-6 grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        {/* COLUMNA 1: CONTROLES */}
        <div className="lg:col-span-1 space-y-6 border-b lg:border-b-0 lg:border-r border-gray-100 pb-6 lg:pb-0 lg:pr-6">
          
          {/* Entrenar */}
          <div>
            <h3 className="font-bold text-gray-700 mb-2">1. Actualizar Cerebro</h3>
            <button
              onClick={handleTrain}
              disabled={loadingTrain}
              className={`w-full py-3 rounded-xl font-bold text-white shadow-lg transition-transform active:scale-95 text-sm
                ${loadingTrain ? 'bg-gray-400' : 'bg-black hover:bg-gray-800'}`}
            >
              {loadingTrain ? 'Procesando...' : '🧠 RE-ENTRENAR MODELO'}
            </button>
          </div>

          {/* Buscar */}
          <div>
            <h3 className="font-bold text-gray-700 mb-2">2. Analizar Usuario</h3>
            <form onSubmit={handlePredict} className="flex gap-2">
              <input 
                type="number" placeholder="ID Usuario" value={searchId}
                onChange={(e) => setSearchId(e.target.value)}
                className="flex-1 border-2 border-gray-200 rounded-lg p-2 outline-none focus:border-indigo-500"
              />
              <button 
                type="submit" disabled={loadingPredict}
                className="bg-indigo-600 text-white px-4 rounded-lg font-bold hover:bg-indigo-700 disabled:bg-indigo-300"
              >
                🔍
              </button>
            </form>
            {error && <p className="text-red-500 text-xs mt-2 font-bold">{error}</p>}
          </div>
        </div>

        {/* COLUMNA 2 y 3: RESULTADOS Y GRÁFICA */}
        <div className="lg:col-span-2">
          {!prediccion && (
            <div className="h-full flex items-center justify-center text-gray-400 italic">
              Introduce un ID para ver el análisis comparativo...
            </div>
          )}

          {prediccion && (
            <div className="animate-fade-in">
              {/* Header Resultado */}
              <div className="flex justify-between items-start mb-6">
                <div>
                  <span className="bg-indigo-100 text-indigo-700 text-xs font-bold px-2 py-1 rounded uppercase tracking-wider">
                    Perfil Detectado
                  </span>
                  <h4 className="text-3xl font-black text-indigo-900 mt-1">{prediccion.perfil_ia}</h4>
                </div>
                <div className="text-right hidden sm:block">
                  <p className="text-xs text-gray-400 uppercase font-bold">Confianza</p>
                  <p className="text-xl font-bold text-green-500">Alta</p>
                </div>
              </div>

              {/* Recomendación */}
              <div className="bg-yellow-50 border-l-4 border-yellow-400 p-4 mb-6 rounded-r">
                <p className="text-sm text-yellow-800 italic">"{prediccion.recomendacion}"</p>
              </div>

              {/* GRÁFICA DE BARRAS */}
              <div className="h-64 w-full">
                <h5 className="text-sm font-bold text-gray-600 mb-4 text-center">TÚ vs PROMEDIO DEL GRUPO</h5>
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart
                    data={prediccion.datosGrafica}
                    margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
                  >
                    <CartesianGrid strokeDasharray="3 3" vertical={false} />
                    <XAxis dataKey="name" tick={{fontSize: 10}} interval={0} />
                    <YAxis tick={{fontSize: 10}} />
                    <Tooltip 
                      contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)' }}
                    />
                    <Legend />
                    <Bar dataKey="Tu" fill="#4f46e5" radius={[4, 4, 0, 0]} name="Tú" />
                    <Bar dataKey="Media" fill="#cbd5e1" radius={[4, 4, 0, 0]} name="Media Grupo" />
                  </BarChart>
                </ResponsiveContainer>
              </div>

            </div>
          )}
        </div>

      </div>
    </div>
  );
};

export default IAControlPanel;