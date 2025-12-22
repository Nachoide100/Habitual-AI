import { useState } from 'react';

const NutricionForm = ({ onSubmit, onCancel }) => {
  const [datos, setDatos] = useState({
    agua_litros: '',
    cheat_meal: false,
    fruta: '',
    verdura: '',
    proteina_animal: '',
    hidratos: ''
  });

  const handleChange = (e) => {
    const valor = e.target.type === 'checkbox' ? e.target.checked : e.target.value;
    setDatos({ ...datos, [e.target.name]: valor });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit({
        agua_litros: parseFloat(datos.agua_litros || 0),
        cheat_meal: datos.cheat_meal,
        fruta: parseInt(datos.fruta || 0),
        verdura: parseInt(datos.verdura || 0),
        proteina_animal: parseInt(datos.proteina_animal || 0),
        hidratos: parseInt(datos.hidratos || 0)
    });
  };

  const inputStyle = "w-full border-b-2 border-gray-200 p-2 focus:border-green-600 outline-none bg-transparent transition-colors text-lg";
  const labelStyle = "block text-xs font-bold text-gray-500 uppercase tracking-wider mb-1";

  return (
    <div className="bg-white p-6 rounded-2xl shadow-lg border border-green-100 h-full flex flex-col">
      <h2 className="text-xl font-black text-gray-800 mb-4">🍎 Nutrición</h2>
      
      <form onSubmit={handleSubmit} className="space-y-4 flex flex-col flex-grow">
        <div className="flex gap-4 items-end">
          <div className="flex-1">
            <label className={labelStyle}>Agua (L)</label>
            <input type="number" step="0.5" name="agua_litros" className={inputStyle} onChange={handleChange} value={datos.agua_litros} placeholder="2.0" />
          </div>
          <div className="flex items-center gap-2 mb-2">
            <input type="checkbox" name="cheat_meal" checked={datos.cheat_meal} onChange={handleChange} className="w-5 h-5 accent-red-500" />
            <span className="text-xs font-bold text-red-500 uppercase">Cheat Meal</span>
          </div>
        </div>

        <p className="text-xs font-bold text-gray-400 mt-2 border-b pb-1">RACIONES</p>
        <div className="grid grid-cols-2 gap-4">
           <div><label className={labelStyle}>Fruta</label><input type="number" name="fruta" className={inputStyle} onChange={handleChange} value={datos.fruta} /></div>
           <div><label className={labelStyle}>Verdura</label><input type="number" name="verdura" className={inputStyle} onChange={handleChange} value={datos.verdura} /></div>
           <div><label className={labelStyle}>Proteína</label><input type="number" name="proteina_animal" className={inputStyle} onChange={handleChange} value={datos.proteina_animal} /></div>
           <div><label className={labelStyle}>Hidratos</label><input type="number" name="hidratos" className={inputStyle} onChange={handleChange} value={datos.hidratos} /></div>
        </div>

        <button type="submit" className="w-full bg-green-600 text-white font-bold py-2 rounded mt-auto hover:bg-green-700 transition-transform active:scale-95">
          Registrar
        </button>
      </form>
    </div>
  );
};
export default NutricionForm;