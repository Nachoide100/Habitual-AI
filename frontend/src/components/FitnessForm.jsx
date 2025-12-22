import { useState } from 'react';

const FitnessForm = () => {
  const [datos, setDatos] = useState({ duracion_minutos: '', distancia_km: '', intensidad: 3, tipo_ejercicio: '' });

  const handleChange = (e) => setDatos({ ...datos, [e.target.name]: e.target.value });
  const handleSubmit = (e) => { e.preventDefault(); alert(`Fitness: ${JSON.stringify(datos)}`); };

  const inputStyle = "w-full border-b-2 border-gray-200 p-2 focus:border-orange-500 outline-none bg-transparent transition-colors text-lg";
  const labelStyle = "block text-xs font-bold text-gray-500 uppercase tracking-wider mb-1";

  return (
    <div className="bg-white p-6 rounded-2xl shadow-lg border border-orange-100 h-full flex flex-col">
      <h2 className="text-xl font-black text-gray-800 mb-4">💪 Deporte</h2>
      
      <form onSubmit={handleSubmit} className="space-y-4 flex flex-col flex-grow">
        <div><label className={labelStyle}>Duración (min)</label><input type="number" name="duracion_minutos" className={inputStyle} onChange={handleChange} value={datos.duracion_minutos} /></div>
        <div><label className={labelStyle}>Distancia (km)</label><input type="number" name="distancia_km" className={inputStyle} onChange={handleChange} value={datos.distancia_km} /></div>
        
        <div>
          <label className={labelStyle}>Intensidad: {datos.intensidad}</label>
          <input type="range" name="intensidad" min="1" max="5" className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-orange-500" onChange={handleChange} value={datos.intensidad} />
        </div>

        <div><label className={labelStyle}>Actividad</label><input type="text" name="tipo_ejercicio" placeholder="Ej: Running" className={inputStyle} onChange={handleChange} value={datos.tipo_ejercicio} /></div>

        <button type="submit" className="w-full bg-orange-500 text-white font-bold py-2 rounded mt-auto hover:bg-orange-600 transition-transform active:scale-95">
          Registrar
        </button>
      </form>
    </div>
  );
};
export default FitnessForm;