import { useState } from 'react';

const OcioForm = () => {
  const [datos, setDatos] = useState({ minutos: '', momento: 'noche', tipo_ocio: 'ver la televisión' });

  const handleChange = (e) => setDatos({ ...datos, [e.target.name]: e.target.value });
  const handleSubmit = (e) => { e.preventDefault(); alert(`Ocio: ${JSON.stringify(datos)}`); };

  const inputStyle = "w-full border-b-2 border-gray-200 p-2 focus:border-black outline-none bg-transparent text-lg";
  const labelStyle = "block text-xs font-bold text-gray-500 uppercase tracking-wider mb-1";

  return (
    <div className="bg-white p-6 rounded-2xl shadow-lg border border-pink-100">
      <h2 className="text-xl font-black text-gray-800 mb-4">🎮 Ocio</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div><label className={labelStyle}>Minutos</label><input type="number" name="minutos" className={inputStyle} onChange={handleChange} value={datos.minutos} /></div>
        <div>
            <label className={labelStyle}>¿Qué actividad?</label>
            <select name="tipo_ocio" className="w-full p-2 bg-pink-50 rounded" onChange={handleChange} value={datos.tipo_ocio}>
                <option value="ver la televisión">TV / Series</option>
                <option value="videojuegos">Videojuegos</option>
                <option value="juego de mesa">Juegos de Mesa</option>
                <option value="hobbies artísiticos">Arte / Hobby</option>
            </select>
        </div>
        <button type="submit" className="w-full bg-pink-600 text-white font-bold py-2 rounded mt-4 hover:bg-pink-700">REGISTRAR</button>
      </form>
    </div>
  );
};
export default OcioForm;