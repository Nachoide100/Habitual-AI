import { useState } from 'react';

const SuenoForm = ({ onSubmit, onCancel }) => {
  const [datos, setDatos] = useState({ horas: '', calidad: 7, madrugar: false });

  const handleChange = (e) => {
    const valor = e.target.type === 'checkbox' ? e.target.checked : e.target.value;
    setDatos({ ...datos, [e.target.name]: valor });
  };
  
  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit({
        horas: parseFloat(datos.horas),
        calidad: parseInt(datos.calidad),
        madrugar: datos.madrugar
    });
  };

  const inputStyle = "w-full border-b-2 border-gray-200 p-2 focus:border-indigo-500 outline-none bg-transparent transition-colors text-lg";
  const labelStyle = "block text-xs font-bold text-gray-500 uppercase tracking-wider mb-1";

  return (
    <div className="bg-white p-6 rounded-2xl shadow-lg border border-indigo-100 h-full flex flex-col">
      <h2 className="text-xl font-black text-gray-800 mb-4">😴 Sueño</h2>
      
      <form onSubmit={handleSubmit} className="space-y-4 flex flex-col flex-grow">
        <div><label className={labelStyle}>Horas</label><input type="number" step="0.5" name="horas" className={inputStyle} onChange={handleChange} value={datos.horas} /></div>
        
        <div>
          <label className={labelStyle}>Calidad: {datos.calidad}</label>
          <input type="range" name="calidad" min="1" max="10" className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-indigo-600" onChange={handleChange} value={datos.calidad} />
        </div>

        <div className="flex items-center gap-2 p-2 bg-indigo-50 rounded">
          <input type="checkbox" name="madrugar" checked={datos.madrugar} onChange={handleChange} className="w-5 h-5 accent-indigo-600" />
          <span className="text-sm font-medium text-indigo-900">¿Has madrugado?</span>
        </div>

        <button type="submit" className="w-full bg-indigo-600 text-white font-bold py-2 rounded mt-auto hover:bg-indigo-700 transition-transform active:scale-95">
          Registrar
        </button>
      </form>
    </div>
  );
};
export default SuenoForm;