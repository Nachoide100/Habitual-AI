import { useState } from 'react';

const SocialForm = ({ onSubmit, onCancel }) => {
  const [datos, setDatos] = useState({ minutos: '', momento: 'tarde', tipo_social: 'amigos' });

  const handleChange = (e) => setDatos({ ...datos, [e.target.name]: e.target.value });
  
  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit({
        minutos: parseInt(datos.minutos),
        momento: datos.momento,
        tipo_social: datos.tipo_social
    });
  };

  const inputStyle = "w-full border-b-2 border-gray-200 p-2 focus:border-blue-600 outline-none bg-transparent text-lg";
  const labelStyle = "block text-xs font-bold text-gray-500 uppercase tracking-wider mb-1";

  return (
    <div className="bg-white p-6 rounded-2xl shadow-lg border border-blue-100 h-full flex flex-col">
      <h2 className="text-xl font-black text-gray-800 mb-4">💬 Social</h2>
      
      <form onSubmit={handleSubmit} className="space-y-4 flex flex-col flex-grow">
        <div><label className={labelStyle}>Minutos</label><input type="number" name="minutos" className={inputStyle} onChange={handleChange} value={datos.minutos} /></div>
        <div>
            <label className={labelStyle}>¿Con quién?</label>
            <select name="tipo_social" className="w-full p-2 bg-blue-50 rounded" onChange={handleChange} value={datos.tipo_social}>
                <option value="familia">Familia</option>
                <option value="amigos">Amigos</option>
                <option value="compañeros de trabajo">Trabajo</option>
            </select>
        </div>
        
        <button type="submit" className="w-full bg-blue-600 text-white font-bold py-2 rounded mt-auto hover:bg-blue-700 transition-transform active:scale-95">
          Registrar
        </button>
      </form>
    </div>
  );
};
export default SocialForm;