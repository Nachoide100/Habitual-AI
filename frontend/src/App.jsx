import LecturaForm from "./components/LecturaForm";
import FitnessForm from "./components/FitnessForm";
import SuenoForm from "./components/SuenoForm";

function App() {
  return (
    <div className="min-h-screen bg-gray-100 p-10">
      <h1 className="text-center text-4xl font-extrabold text-gray-800 mb-2">Mis Formularios</h1>
      <p className="text-center text-gray-400 mb-10">Probando los diseños paso a paso</p>
      
      {/* Grid para verlos uno al lado del otro */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        
        {/* Columna 1 */}
        <LecturaForm />
        
        {/* Columna 2 */}
        <FitnessForm />
        
        {/* Columna 3 */}
        <SuenoForm />

      </div>
    </div>
  );
}

export default App;