# 🧠 Habitual AI: Smart Habit Tracker & Profiler

![Project Status](https://img.shields.io/badge/Status-Completed-success)
![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python&logoColor=white)
![React](https://img.shields.io/badge/React-18-61DAFB?logo=react&logoColor=black)
![FastAPI](https://img.shields.io/badge/FastAPI-0.95+-009688?logo=fastapi&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/ML-Scikit--Learn-F7931E?logo=scikit-learn&logoColor=white)

> **Más que un simple registro de hábitos.** Habitual AI es una plataforma Full-Stack que utiliza algoritmos de Machine Learning no supervisado para perfilar usuarios y generar comparativas de rendimiento (Benchmarking) en tiempo real contra grupos demográficos similares.

---

## 📸 Vistazo Rápido


![Dashboard Preview](https://github.com/Nachoide100/Habitual-AI/blob/ce89ade07843d676d2268cea6359f7d3ec0f5f06/visualizations/Captura%20de%20pantalla%202026-01-06%20121835.png)

---

## 🚀 Características Clave

### 1. ⚛️ Frontend Reactivo & Modular
- **Arquitectura de Componentes:** Formularios independientes y reutilizables para métricas dispares (Fitness, Nutrición, Mindfulness, Ocio, Vicios...).
  
  ![Formulario Lectura](https://github.com/Nachoide100/Habitual-AI/blob/ce89ade07843d676d2268cea6359f7d3ec0f5f06/visualizations/Captura%20de%20pantalla%202026-01-06%20121328.png)
  ![Formulario Estado de ánimo](https://github.com/Nachoide100/Habitual-AI/blob/e2420f1051ed0a070e6e165dad47685ec5ade0f0/visualizations/Captura%20de%20pantalla%202026-01-06%20122629.png)
 
- **Visualización de Datos:** Integración de **Recharts** para renderizar gráficas comparativas complejas.
- **UX Dinámica:** Feedback en tiempo real, validación de formularios y manejo de estados de carga/error asíncronos.

### 2. 🐍 Backend Robusto (FastAPI)
- **API RESTful:** Endpoints tipados y validados con **Pydantic**.
- **Persistencia:** Base de datos SQLite gestionada con **SQLAlchemy ORM**.
- **Gestión de Errores:** Sistema de excepciones personalizado para asegurar la estabilidad del servidor.

### 3. 🤖 El Cerebro: Motor de IA (K-Means)
El núcleo diferenciador del proyecto. No usa reglas fijas, sino que "aprende" de la población.
- **Algoritmo:** Clustering **K-Means** para agrupar usuarios automáticamente.
- **Preprocesamiento:** Pipeline con **StandarScaler** para normalizar datos y manejar outliers.
- **Etiquetado Inteligente:** Lógica *"King of the Hill"* para asignar etiquetas semánticas (Gamer, Deportista, Ejecutivo, Senior) basándose en los centroides de los clústeres.
- **Benchmarking:** Cálculo estadístico en tiempo real para comparar al usuario activo vs. la media de su clúster asignado.

### 4. 🧬 Simulación de Datos (Data Seeding)
Solución al problema del "Cold Start".
- Script avanzado con **Faker** que genera usuarios sintéticos con métricas basadas en sus estilos de vida. 
- Simulación de  **historial biométrico y conductual** coherente para cada perfil (ej: los "Estudiantes" generados tienen mayor ocio nocturno en findes de semana).

---

## 🛠️ Stack Tecnológico

| Área | Tecnologías |
|------|-------------|
| **Frontend** | React, Vite, Tailwind CSS, Recharts |
| **Backend** | Python, FastAPI, Uvicorn |
| **Data Science** | Pandas, NumPy, Scikit-learn, Joblib |
| **Database** | SQLite, SQLAlchemy |

---

## 📊 Visualización de Datos

El sistema permite al usuario conocer a que perfil pertenece y entender su posición en el grupo mediante gráficas comparativas directas:


![Gráfica Comparativa](https://github.com/Nachoide100/Habitual-AI/blob/e69003dc5a729cab0b480ec6609d0408e594d14d/visualizations/Captura%20de%20pantalla%202026-01-06%20122855.png)
![Gráfica Comparativa](https://github.com/Nachoide100/Habitual-AI/blob/e69003dc5a729cab0b480ec6609d0408e594d14d/visualizations/Captura%20de%20pantalla%202026-01-06%20122920.png)

---

## ⚙️ Instalación y Despliegue Local

Sigue estos pasos para levantar el proyecto en tu máquina:

### 1. Clonar el repositorio
```bash
git clone [https://github.com/tu-usuario/habitual-ai.git](https://github.com/tu-usuario/habitual-ai.git)
cd habitual-ai
```
### 2. Configurar el Backend
```bash
cd Backend
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```
### 3. Poblar la base de datos
Aquí podemos elegir cuántos usuarios y durante cuanto tiempo queremos hacer la simulación.
```bash
python seeder.py
```
### 4. Iniciar el servidor
```bash
uvicorn main:app --reload
```
### 5. Configurar el frontend
```bash
cd frontend
npm install
npm run dev
```






