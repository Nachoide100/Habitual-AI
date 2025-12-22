import { useState } from 'react';

const ViciosForm = ({ onSubmit, onCancel }) => {
  const [datos, setDatos] = useState({ tabaco: '', alcohol: '', sedentarismo: '' });

  const handleChange = (e) => setDatos({ ...datos, [e.target.name]: e.target.value });
  
  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit({
        tabaco: parseInt(datos.tabaco || 0),
        alcohol: parseInt(datos.alcohol || 0),
        sedentarismo: parseInt(datos.sedentarismo || 0)
    });
  };

  const inputStyle = "w-full border-b-2 border-gray-200 p-2 focus:border-red-600 outline-none bg-transparent text-lg";
  const labelStyle = "block text-xs font-bold text-gray-500 uppercase tracking-wider mb-1";

  return (
    <div className="bg-white p-6 rounded-2xl shadow-lg border border-red-100 h-full flex flex-col">
      <h2 className="text-xl font-black text-gray-800 mb-4">🍷 Hábitos -</h2>
      
      <form onSubmit={handleSubmit} className="space-y-4 flex flex-col flex-grow">
        <div><label className={labelStyle}>Cigarrillos</label><input type="number" name="tabaco" className={inputStyle} onChange={handleChange} value={datos.tabaco} placeholder="0" /></div>
        <div><label className={labelStyle}>Alcohol (Unidades)</label><input type="number" name="alcohol" className={inputStyle} onChange={handleChange} value={datos.alcohol} placeholder="0" /></div>
        <div><label className={labelStyle}>Horas Sentado</label><input type="number" name="sedentarismo" className={inputStyle} onChange={handleChange} value={datos.sedentarismo} placeholder="8" /></div>
        
        <button type="submit" className="w-full bg-red-600 text-white font-bold py-2 rounded mt-auto hover:bg-red-700 transition-transform active:scale-95">
          Registrar
        </button>
      </form>
    </div>
  );
};
export default ViciosForm;