import { useState } from 'react';

const EstadoAnimoForm = ({ onSubmit, onCancel }) => {
  const [datos, setDatos] = useState({ puntuacion_dia: 7, nivel_energia: 7, notas: '' });

  const handleChange = (e) => setDatos({ ...datos, [e.target.name]: e.target.value });
  
  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit({
        puntuacion_dia: parseInt(datos.puntuacion_dia),
        nivel_energia: parseInt(datos.nivel_energia),
        notas: datos.notas
    });
  };

  const labelStyle = "block text-xs font-bold text-gray-500 uppercase tracking-wider mb-1";

  return (
    <div className="bg-white p-6 rounded-2xl shadow-lg border border-yellow-100 h-full flex flex-col">
      <h2 className="text-xl font-black text-gray-800 mb-4">🙂 Estado de Ánimo</h2>
      
      <form onSubmit={handleSubmit} className="space-y-4 flex flex-col flex-grow">
        <div>
           <label className={labelStyle}>¿Qué tal el día? (1-10): <span className="text-xl text-yellow-500">{datos.puntuacion_dia}</span></label>
           <input type="range" name="puntuacion_dia" min="1" max="10" className="w-full accent-yellow-500" onChange={handleChange} value={datos.puntuacion_dia} />
        </div>

        <div>
           <label className={labelStyle}>Energía (1-10): <span className="text-xl text-blue-500">{datos.nivel_energia}</span></label>
           <input type="range" name="nivel_energia" min="1" max="10" className="w-full accent-blue-500" onChange={handleChange} value={datos.nivel_energia} />
        </div>

        <div>
          <label className={labelStyle}>Notas del día</label>
          <textarea name="notas" rows="2" className="w-full border p-2 rounded bg-yellow-50" placeholder="Hoy me sentí..." onChange={handleChange} value={datos.notas} />
        </div>

        <button type="submit" className="w-full bg-yellow-500 text-white font-bold py-2 rounded mt-auto hover:bg-yellow-600 transition-transform active:scale-95">
          Registrar
        </button>
      </form>
    </div>
  );
};
export default EstadoAnimoForm;