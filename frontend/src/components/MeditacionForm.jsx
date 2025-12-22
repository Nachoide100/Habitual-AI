import { useState } from 'react';

const MeditacionForm = () => {
  const [datos, setDatos] = useState({ minutos: '', momento: 'mañana', estres_antes: 5, estres_despues: 3 });

  const handleChange = (e) => setDatos({ ...datos, [e.target.name]: e.target.value });
  const handleSubmit = (e) => { e.preventDefault(); alert(`Meditación: ${JSON.stringify(datos)}`); };

  const inputStyle = "w-full border-b-2 border-gray-200 p-2 focus:border-purple-600 outline-none bg-transparent text-lg";
  const labelStyle = "block text-xs font-bold text-gray-500 uppercase tracking-wider mb-1";

  return (
    <div className="bg-white p-6 rounded-2xl shadow-lg border border-purple-100 h-full flex flex-col">
      <h2 className="text-xl font-black text-gray-800 mb-4">🧘‍♀️ Meditación</h2>
      
      <form onSubmit={handleSubmit} className="space-y-4 flex flex-col flex-grow">
        <div><label className={labelStyle}>Minutos</label><input type="number" name="minutos" className={inputStyle} onChange={handleChange} value={datos.minutos} /></div>
        <div>
          <label className={labelStyle}>Momento</label>
          <select name="momento" className="w-full p-2 bg-purple-50 rounded outline-none" onChange={handleChange} value={datos.momento}>
            <option value="mañana">Mañana</option><option value="tarde">Tarde</option><option value="noche">Noche</option>
          </select>
        </div>
        
        <div className="grid grid-cols-2 gap-4 mt-4">
          <div className="text-center">
            <label className="text-xs font-bold text-red-400">ANTES: {datos.estres_antes}</label>
            <input type="range" name="estres_antes" min="1" max="10" className="w-full accent-red-400" onChange={handleChange} value={datos.estres_antes} />
          </div>
          <div className="text-center">
            <label className="text-xs font-bold text-green-500">DESPUÉS: {datos.estres_despues}</label>
            <input type="range" name="estres_despues" min="1" max="10" className="w-full accent-green-500" onChange={handleChange} value={datos.estres_despues} />
          </div>
        </div>

        <button type="submit" className="w-full bg-purple-600 text-white font-bold py-2 rounded mt-auto hover:bg-purple-700 transition-transform active:scale-95">
          Registrar
        </button>
      </form>
    </div>
  );
};
export default MeditacionForm;