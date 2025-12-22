import { useState } from 'react';

const SuenoForm = () => {
  const [datos, setDatos] = useState({
    horas: '',
    calidad: 7,
    madrugar: false
  });

  const handleChange = (e) => {
    // Si es checkbox usamos 'checked', si no usamos 'value'
    const valor = e.target.type === 'checkbox' ? e.target.checked : e.target.value;
    setDatos({ ...datos, [e.target.name]: valor });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    alert(`Sueño: ${JSON.stringify(datos)}`);
  };

  const inputStyle = "w-full border-b-2 border-gray-200 p-2 focus:border-black outline-none bg-transparent transition-colors text-lg";
  const labelStyle = "block text-xs font-bold text-gray-500 uppercase tracking-wider mb-1";

  return (
    <div className="max-w-sm mx-auto bg-white p-8 rounded-2xl shadow-xl mt-6">
      <h2 className="text-2xl font-black text-gray-800 mb-6">Registrar Sueño 😴</h2>
      
      <form onSubmit={handleSubmit} className="space-y-6">
        
        {/* Horas */}
        <div>
          <label className={labelStyle}>Horas dormidas</label>
          <input type="number" step="0.5" name="horas" className={inputStyle} onChange={handleChange} value={datos.horas} placeholder="7.5" />
        </div>

        {/* Calidad (Slider 1-10) */}
        <div>
          <label className={labelStyle}>Calidad (1-10): <span className="text-black text-lg">{datos.calidad}</span></label>
          <input type="range" name="calidad" min="1" max="10" className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-indigo-500" onChange={handleChange} value={datos.calidad} />
        </div>

        {/* Madrugar (CHECKBOX) */}
        <div className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg border border-gray-100">
          <input 
            type="checkbox" 
            name="madrugar" 
            checked={datos.madrugar}
            onChange={handleChange}
            className="w-5 h-5 text-black border-gray-300 rounded focus:ring-black accent-black"
          />
          <label className="text-sm font-medium text-gray-700">¿He madrugado hoy?</label>
        </div>

        <button type="submit" className="w-full bg-black text-white font-bold py-3 rounded-lg hover:bg-gray-800 transition-transform active:scale-95">
          GUARDAR SUEÑO
        </button>
      </form>
    </div>
  );
};

export default SuenoForm;