import { useState } from 'react';

const FitnessForm = () => {
  const [datos, setDatos] = useState({
    duracion_minutos: '',
    distancia_km: '',
    intensidad: 3, // Valor por defecto (medio)
    tipo_ejercicio: 'cardio'
  });

  const handleChange = (e) => {
    setDatos({ ...datos, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    alert(`Fitness: ${JSON.stringify(datos)}`);
  };

  // Estilos reutilizables (Mismo diseño que Lectura)
  const inputStyle = "w-full border-b-2 border-gray-200 p-2 focus:border-black outline-none bg-transparent transition-colors text-lg";
  const labelStyle = "block text-xs font-bold text-gray-500 uppercase tracking-wider mb-1";

  return (
    <div className="max-w-sm mx-auto bg-white p-8 rounded-2xl shadow-xl mt-6">
      <h2 className="text-2xl font-black text-gray-800 mb-6">Registrar Deporte 💪</h2>
      
      <form onSubmit={handleSubmit} className="space-y-6">
        
        {/* Duración */}
        <div>
          <label className={labelStyle}>Duración (min)</label>
          <input type="number" name="duracion_minutos" className={inputStyle} onChange={handleChange} value={datos.duracion_minutos} placeholder="0" />
        </div>

        {/* Distancia */}
        <div>
          <label className={labelStyle}>Distancia (km)</label>
          <input type="number" step="0.1" name="distancia_km" className={inputStyle} onChange={handleChange} value={datos.distancia_km} placeholder="0.0" />
        </div>

        {/* Intensidad (SLIDER) */}
        <div>
          <label className={labelStyle}>Intensidad (1-5): <span className="text-black text-lg">{datos.intensidad}</span></label>
          <input 
            type="range" 
            name="intensidad" 
            min="1" max="5" 
            className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-black"
            onChange={handleChange} 
            value={datos.intensidad} 
          />
          <div className="flex justify-between text-xs text-gray-400 mt-1">
            <span>Suave</span><span>Intenso</span>
          </div>
        </div>

        {/* Tipo Ejercicio */}
        <div>
          <label className={labelStyle}>Tipo</label>
          <input type="text" name="tipo_ejercicio" className={inputStyle} onChange={handleChange} value={datos.tipo_ejercicio} placeholder="Ej: Running, Gimnasio..." />
        </div>

        <button type="submit" className="w-full bg-black text-white font-bold py-3 rounded-lg hover:bg-gray-800 transition-transform active:scale-95">
          GUARDAR ENTRENO
        </button>
      </form>
    </div>
  );
};

export default FitnessForm;