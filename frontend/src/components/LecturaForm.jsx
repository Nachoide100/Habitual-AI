import { useState } from 'react';

const LecturaForm = () => {
  const [datos, setDatos] = useState({ paginas: '', minutos: '', categoria: 'ficcion' });

  const handleChange = (e) => setDatos({ ...datos, [e.target.name]: e.target.value });
  const handleSubmit = (e) => { e.preventDefault(); alert(`Lectura: ${JSON.stringify(datos)}`); };

  const inputStyle = "w-full border-b-2 border-gray-200 p-2 focus:border-cyan-500 outline-none bg-transparent transition-colors text-lg";
  const labelStyle = "block text-xs font-bold text-gray-500 uppercase tracking-wider mb-1";

  return (
    // CAMBIO 1: Añadimos 'h-full flex flex-col' al div principal
    <div className="bg-white p-6 rounded-2xl shadow-lg border border-cyan-100 h-full flex flex-col">
      <h2 className="text-xl font-black text-gray-800 mb-4">📖 Lectura</h2>
      
      {/* CAMBIO 2: Añadimos 'flex flex-col flex-grow' al form */}
      <form onSubmit={handleSubmit} className="space-y-4 flex flex-col flex-grow">
        
        <div><label className={labelStyle}>Páginas</label><input type="number" name="paginas" className={inputStyle} onChange={handleChange} value={datos.paginas} /></div>
        <div><label className={labelStyle}>Minutos</label><input type="number" name="minutos" className={inputStyle} onChange={handleChange} value={datos.minutos} /></div>
        
        <div>
          <label className={labelStyle}>Categoría</label>
          <select name="categoria" className="w-full p-2 bg-cyan-50 rounded focus:outline-none focus:ring-2 focus:ring-cyan-200" onChange={handleChange} value={datos.categoria}>
            <option value="ficcion">Ficción</option>
            <option value="no_ficcion">No Ficción</option>
            <option value="desarrollo">Desarrollo</option>
            <option value="otro">Otro</option>
          </select>
        </div>

        {/* CAMBIO 3: Añadimos 'mt-auto' al botón */}
        <button type="submit" className="w-full bg-cyan-600 text-white font-bold py-2 rounded mt-auto hover:bg-cyan-700 transition-transform active:scale-95">
          Registrar
        </button>
      </form>
    </div>
  );
};
export default LecturaForm;