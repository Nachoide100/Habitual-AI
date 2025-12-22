import { useState, useEffect } from 'react';

// Importamos todos tus formularios
import LecturaForm from './LecturaForm';
import FitnessForm from './FitnessForm';
import SuenoForm from './SuenoForm';
import NutricionForm from './NutricionForm';
import ViciosForm from './ViciosForm';
import MeditacionForm from './MeditacionForm';
import EstadoAnimoForm from './EstadoAnimoForm';
import SocialForm from './SocialForm';
import OcioForm from './OcioForm';

const MisHabitos = () => {
  const USUARIO_ID = 1; // De momento trabajamos con el usuario 1

  const [habitos, setHabitos] = useState([]); // Lista de hábitos de la BD
  const [habitoSeleccionado, setHabitoSeleccionado] = useState(null); // ¿Qué formulario está abierto?

  // 1. CARGAR HÁBITOS DE LA API (AL INICIAR)
  useEffect(() => {
    fetch(`http://127.0.0.1:8000/usuarios/${USUARIO_ID}/habitos/`)
      .then(response => response.json())
      .then(data => setHabitos(data))
      .catch(error => console.error("Error cargando hábitos:", error));
  }, []);

  // 2. FUNCIÓN PARA GUARDAR EN LA BASE DE DATOS
  const guardarRegistro = async (datosFormulario) => {
    if (!habitoSeleccionado) return;

    try {
      // Llamada POST a tu API
      const response = await fetch(`http://127.0.0.1:8000/habitos/${habitoSeleccionado.id}/entradas/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        // TU SCHEMA ESPERA UN CAMPO "valor" CON EL JSON DENTRO
        body: JSON.stringify({
          valor: datosFormulario 
        })
      });

      if (response.ok) {
        alert("✅ ¡Guardado correctamente!");
        setHabitoSeleccionado(null); // Cerrar formulario
      } else {
        const errorData = await response.json();
        alert(`❌ Error: ${errorData.detail}`);
      }
    } catch (error) {
      alert("Error de conexión con el servidor");
    }
  };

  // 3. DICCIONARIO PARA ELEGIR FORMULARIO
  // Según el "tipo_habito" que viene de la BD, elegimos qué componente pintar
  const renderizarFormulario = () => {
    if (!habitoSeleccionado) return null;

    const propsComunes = {
      onSubmit: guardarRegistro,
      onCancel: () => setHabitoSeleccionado(null)
    };

    switch (habitoSeleccionado.tipo_habito) {
      case 'lectura': return <LecturaForm {...propsComunes} />;
      case 'fitness': return <FitnessForm {...propsComunes} />;
      case 'sueno': return <SuenoForm {...propsComunes} />;
      case 'nutricion': return <NutricionForm {...propsComunes} />;
      case 'habito_no_saludable': return <ViciosForm {...propsComunes} />;
      case 'meditacion': return <MeditacionForm {...propsComunes} />;
      case 'estado_animo': return <EstadoAnimoForm {...propsComunes} />;
      case 'actividad_social': return <SocialForm {...propsComunes} />;
      case 'actividad_ocio': 
      case 'ocio': return <OcioForm {...propsComunes} />; // Por si en la BD se llama de una forma u otra
      default: return <p>Formulario no disponible</p>;
    }
  };

  return (
    <div className="p-8 bg-gray-50 min-h-screen">
      <h1 className="text-3xl font-bold text-gray-800 mb-8 text-center">Mis Hábitos Diarios</h1>

      {/* SI HAY UN FORMULARIO ABIERTO, LO MOSTRAMOS EN UNA VENTANA MODAL */}
      {habitoSeleccionado && (
        <div 
          className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50"
          // 1. AQUÍ ESTÁ EL TRUCO: Si haces clic en lo negro, se cierra
          onClick={() => setHabitoSeleccionado(null)}
        >
          <div 
            className="w-full max-w-md"
            // 2. IMPORTANTE: Evitamos que el clic dentro del formulario cierre la ventana
            onClick={(e) => e.stopPropagation()}
          >
             {/* Aquí se pinta el formulario específico */}
             {renderizarFormulario()}
          </div>
        </div>
      )}
      {/* LISTA DE BOTONES (Uno por cada hábito que tengas en la BD) */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {habitos.map(habito => (
          <div key={habito.id} className="bg-white p-6 rounded-xl shadow-sm hover:shadow-md transition-shadow border border-gray-100 flex justify-between items-center">
            <div>
              <h3 className="font-bold text-gray-700">{habito.nombre}</h3>
              <p className="text-xs text-gray-400 uppercase">{habito.tipo_habito}</p>
            </div>
            <button 
              onClick={() => setHabitoSeleccionado(habito)}
              className="bg-black text-white px-4 py-2 rounded-lg text-sm font-bold hover:bg-gray-800"
            >
              REGISTRAR
            </button>
          </div>
        ))}
      </div>
    </div>
  );
};

export default MisHabitos;