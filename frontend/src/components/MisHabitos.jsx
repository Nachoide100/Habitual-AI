import { useState, useEffect } from 'react';
import IAControlPanel from './IAControlPanel';
import LecturaForm from './LecturaForm';
import FitnessForm from './FitnessForm';
import SuenoForm from './SuenoForm';
import NutricionForm from './NutricionForm';
import ViciosForm from './ViciosForm';
import MeditacionForm from './MeditacionForm';
import EstadoAnimoForm from './EstadoAnimoForm';
import SocialForm from './SocialForm';
import OcioForm from './OcioForm'; // Importación de los formularios y archivos necesarios


const MisHabitos = () => {
  const USUARIO_ID = 1; 

  const [habitos, setHabitos] = useState([]); 
  const [habitoSeleccionado, setHabitoSeleccionado] = useState(null); 

  // DICCIONARIO PARA TRADUCIR CATEGORÍAS
  const nombresBonitos = {
    lectura: "Lectura y Aprendizaje",
    fitness: "Ejercicio Físico",
    sueno: "Descanso y Recuperación",
    nutricion: "Alimentación Saludable",
    habito_no_saludable: "Control de Vicios",
    meditacion: "Mindfulness y Relax",
    estado_animo: "Salud Emocional",
    actividad_social: "Vida Social",
    actividad_ocio: "Ocio y Hobbies",
    ocio: "Ocio y Hobbies",
    // Traducimos el hábito de trabajo para que tenga sentido con el form de vicios
    habito_saludable: "Jornada Laboral (Sedentarismo)" 
  };

  // 1. CARGAR HÁBITOS DESDE EL BACKEND
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
      const response = await fetch(`http://127.0.0.1:8000/habitos/${habitoSeleccionado.id}/entradas/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          valor: datosFormulario 
        })
      });

      if (response.ok) { // Mostrar mensaje de éxito por pantall
        alert("✅ ¡Guardado correctamente!");
        setHabitoSeleccionado(null); 
      } else {
        const errorData = await response.json();
        alert(`❌ Error: ${errorData.detail}`); // Control de errores
      }
    } catch (error) {
      alert("Error de conexión con el servidor");
    }
  };

  // 3. DICCIONARIO PARA ELEGIR FORMULARIO SEGÚN EL HÁBITO
  const renderizarFormulario = () => {
    if (!habitoSeleccionado) return null;

    const propsComunes = {
      onSubmit: guardarRegistro,
      onCancel: () => setHabitoSeleccionado(null)
    };

    switch (habitoSeleccionado.tipo_habito) { // Un formulario por cada tipo
      case 'lectura': return <LecturaForm {...propsComunes} />;
      case 'fitness': return <FitnessForm {...propsComunes} />;
      case 'sueno': return <SuenoForm {...propsComunes} />;
      case 'nutricion': return <NutricionForm {...propsComunes} />;
      case 'habito_no_saludable': return <ViciosForm {...propsComunes} />;
      case 'meditacion': return <MeditacionForm {...propsComunes} />;
      case 'estado_animo': return <EstadoAnimoForm {...propsComunes} />;
      case 'actividad_social': return <SocialForm {...propsComunes} />;
      case 'habito_saludable': return <ViciosForm {...propsComunes} />; // Para regisrar sedentarismo
      case 'ocio': return <OcioForm {...propsComunes} />;
      
      default: return <p className="p-4 text-red-500">Formulario no disponible para: {habitoSeleccionado.tipo_habito}</p>;
    }
  };

  return (
    <div className="p-8 bg-gray-50 min-h-screen">
      <h1 className="text-3xl font-bold text-gray-800 mb-8 text-center">Mis Hábitos Diarios</h1>

      {/* --- PANEL DE INTELIGENCIA ARTIFICIAL --- */}
      <div className="max-w-5xl mx-auto mb-10">
        <IAControlPanel />
      </div>

      {/* --- VENTANA MODAL (FORMULARIO) --- */}
      {habitoSeleccionado && (
        <div 
          className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50 animate-fade-in"
          onClick={() => setHabitoSeleccionado(null)} // Cierra al hacer clic fuera
        >
          <div 
            className="w-full max-w-md transform transition-all scale-100"
            onClick={(e) => e.stopPropagation()} // Evita cierre al hacer clic dentro
          >
             {renderizarFormulario()}
          </div>
        </div>
      )}

      {/* --- GRID DE HÁBITOS --- */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 max-w-5xl mx-auto">
        {habitos.map(habito => (
          <div key={habito.id} className="bg-white p-6 rounded-xl shadow-sm hover:shadow-lg transition-all border border-gray-100 flex flex-col justify-between h-32">
            <div>
              <h3 className="text-lg font-bold text-gray-800">{habito.nombre}</h3>
              <p className="text-xs font-medium text-cyan-600 mt-1">
                {nombresBonitos[habito.tipo_habito] || habito.tipo_habito}
              </p>
            </div>
            <button 
              onClick={() => setHabitoSeleccionado(habito)}
              className="mt-auto bg-black text-white px-4 py-2 rounded-lg text-sm font-bold hover:bg-gray-800 transition-colors w-full"
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