import LecturaForm from "./components/LecturaForm";
import FitnessForm from "./components/FitnessForm";
import SuenoForm from "./components/SuenoForm";
import NutricionForm from "./components/NutricionForm";
import ViciosForm from "./components/ViciosForm";
import MeditacionForm from "./components/MeditacionForm";
import EstadoAnimoForm from "./components/EstadoAnimoForm";
import SocialForm from "./components/SocialForm";
import OcioForm from "./components/OcioForm";

function App() {
  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <h1 className="text-center text-4xl font-extrabold text-gray-800 mb-2">Galería de Formularios 🎨</h1>
      <p className="text-center text-gray-400 mb-10">Todos los componentes listos para usar</p>
      
      {/* Grid responsivo: 1 col en móvil, 2 en tablet, 3 en PC */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 max-w-7xl mx-auto">
        
        <LecturaForm />
        <FitnessForm />
        <SuenoForm />
        
        <NutricionForm />
        <MeditacionForm />
        <EstadoAnimoForm />
        
        <SocialForm />
        <OcioForm />
        <ViciosForm />

      </div>
    </div>
  );
}

export default App;