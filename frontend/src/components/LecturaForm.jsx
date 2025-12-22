import { useState } from 'react';

const LecturaForm = () => {
  // 1. Estado para guardar lo que escribe el usuario
  const [datos, setDatos] = useState({
    paginas: '',
    minutos: '',
    categoria: 'ficcion'
  });

  // 2. Función que actualiza el estado cuando escribes
  const handleChange = (e) => {
    setDatos({
      ...datos,
      [e.target.name]: e.target.value
    });
  };

  // 3. Función temporal para ver si funciona (luego la conectaremos al backend)
  const handleSubmit = (e) => {
    e.preventDefault();
    alert(`Datos capturados: ${JSON.stringify(datos)}`);
  };

  // Estilos comunes para no repetir código
  const inputStyle = "w-full border-b-2 border-gray-200 p-2 focus:border-black outline-none bg-transparent transition-colors text-lg";
  const labelStyle = "block text-xs font-bold text-gray-500 uppercase tracking-wider mb-1";

  return (
    <div className="max-w-sm mx-auto bg-white p-8 rounded-2xl shadow-xl mt-10">
      <h2 className="text-2xl font-black text-gray-800 mb-6">Registrar Lectura 📖</h2>
      
      <form onSubmit={handleSubmit} className="space-y-6">
        
        {/* Input Páginas */}
        <div>
          <label className={labelStyle}>Páginas leídas</label>
          <input 
            type="number" 
            name="paginas"
            placeholder="0"
            className={inputStyle}
            onChange={handleChange}
            value={datos.paginas}
          />
        </div>

        {/* Input Minutos */}
        <div>
          <label className={labelStyle}>Tiempo (minutos)</label>
          <input 
            type="number" 
            name="minutos"
            placeholder="0"
            className={inputStyle}
            onChange={handleChange}
            value={datos.minutos}
          />
        </div>

        {/* Select Categoría */}
        <div>
          <label className={labelStyle}>Categoría</label>
          <select 
            name="categoria"
            className="w-full border-b-2 border-gray-200 p-2 bg-white focus:border-black outline-none"
            onChange={handleChange}
            value={datos.categoria}
          >
            <option value="ficcion">Ficción</option>
            <option value="no_ficcion">No Ficción</option>
            <option value="desarrollo">Desarrollo Personal</option>
            <option value="terror">Terror</option>
            <option value="romantico">Romántico</option>
            <option value="historico">Histórico</option>
            <option value="otro">Otro</option>
          </select>
        </div>

        {/* Botón */}
        <button 
          type="submit"
          className="w-full bg-black text-white font-bold py-3 rounded-lg hover:bg-gray-800 transition-transform active:scale-95"
        >
          GUARDAR REGISTRO
        </button>
      </form>
    </div>
  );
};

export default LecturaForm;