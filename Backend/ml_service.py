import pandas as pd
import numpy as np
from sqlalchemy.orm import Session
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import joblib
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt
import os
import models
from database import SessionLocal

# Configuración
MODEL_PATH = "ml_models" 
if not os.path.exists(MODEL_PATH):
    os.makedirs(MODEL_PATH)


# 1. INGENIERÍA DE CARACTERÍSTICAS (

def extraer_metricas_usuario(usuario):
    # 1. Calcular IMC
    altura_m = usuario.altura / 100 #fórmula
    if altura_m == 0: altura_m = 1.70 # Evitar división por cero
    imc = usuario.peso / (altura_m * altura_m)

    # 2. Inicializar métricas
    datos = {
        "edad": usuario.edad,
        "imc": round(imc, 2),
        "sueno_horas": 0,
        "fitness_km": 0,
        "fitness_intensidad": 0,
        "lectura_paginas": 0,
        "ocio_digital_min": 0,  # TV + Videojuegos 
        "sedentarismo_horas": 0, # Clave Ejecutivo/Estudiante
        "nutricion_score": 0,  
        "vicios_score": 0,      # Alcohol + Tabaco
        "estres_promedio": 0
    }

    counts = {k: 0 for k in datos.keys()}

    # 3. Procesar historial
    for habito in usuario.habitos:
        for entrada in habito.entradas:
            val = entrada.valor # JSON

            if habito.tipo_habito == "sueno":
                datos["sueno_horas"] += val.get("horas", 0)
                counts["sueno_horas"] += 1

            elif habito.tipo_habito == "fitness":
                datos["fitness_km"] += val.get("distancia_km", 0)
                datos["fitness_intensidad"] += val.get("intensidad", 1)
                counts["fitness_km"] += 1
                counts["fitness_intensidad"] += 1

            elif habito.tipo_habito == "lectura":
                datos["lectura_paginas"] += val.get("paginas", 0)
                counts["lectura_paginas"] += 1

            elif habito.tipo_habito == "actividad_ocio":
                tipo = val.get("tipo_ocio", "")
                if "videojuegos" in tipo or "televisión" in tipo:
                    datos["ocio_digital_min"] += val.get("minutos", 0)
                    counts["ocio_digital_min"] += 1

            elif habito.tipo_habito == "nutricion":
                puntos = val.get("fruta", 0) + val.get("verdura", 0) + val.get("proteina_animal", 0) + val.get("hidratos", 0)
                if val.get("cheat_meal", False): puntos -= 1
                datos["nutricion_score"] += puntos
                counts["nutricion_score"] += 1

            elif habito.tipo_habito == "habito_saludable":
                datos["sedentarismo_horas"] += val.get("sedentarismo", 0)
                counts["sedentarismo_horas"] += 1

                vicio = val.get("alcohol", 0) + val.get("tabaco", 0)
                datos["vicios_score"] += vicio
                counts["vicios_score"] += 1

            elif habito.tipo_habito == "meditacion":
                datos["estres_promedio"] += val.get("estres_antes", 0)
                counts["estres_promedio"] += 1

    # 4. Promedios finales
    fila_procesada = {}
    for key, value in datos.items():
        if key in ["edad", "imc"]:
            fila_procesada[key] = value
        elif counts[key] > 0:
            fila_procesada[key] = round(value / counts[key], 2)
        else:
            fila_procesada[key] = 0
    return fila_procesada


def obtener_dataset_completo(db: Session):
    print("Generando el dataset...")
    usuarios = db.query(models.Usuario).all()
    data = [extraer_metricas_usuario(u) for u in usuarios]
    df = pd.DataFrame(data).fillna(0)
    return df


# 2. RECOMENDACIONES

def generar_consejo_salud(nombre_perfil):

    consejos = {
        "GAMER": "Detectamos alto sedentarismo y ocio digital. Intenta aplicar la regla 20-20-20 para la vista y camina 10 min por cada hora de juego.",
        "DEPORTISTA": "Tu nivel de actividad es óptimo. Enfócate en la recuperación y la calidad del sueño para evitar lesiones.",
        "SENIOR": "Mantienes una rutina saludable. Sigue con los paseos diarios y vigila la ingesta de proteínas para mantener masa muscular.",
        "EJECUTIVO": "Niveles de estrés y vicios detectados. Prioriza desconectar del trabajo 1 hora antes de dormir y reduce el tabaco.",
        "ESTUDIANTE": "Tu horario de sueño es irregular. Intenta mantener horarios fijos incluso en época de exámenes para mejorar el rendimiento."
    }
    return consejos.get(nombre_perfil, "Sigue registrando hábitos para recibir consejos personalizados.")


# 3. ENTRENAMIENTO DEL ML

def entrenar_modelo(db: Session):
    df = obtener_dataset_completo(db)
    if df.empty:
        print("⚠️ Error: BD vacía.")
        return

    # Features para el Clustering
    features_cols = [
        "edad", "fitness_km", "fitness_intensidad",
        "lectura_paginas", "ocio_digital_min",
        "sedentarismo_horas", "nutricion_score", "vicios_score", 
    ]

    # Features que se verán en el Frontend
    frontend_cols = features_cols + ["imc", "sueno_horas", "estres_promedio"]

    # Estándarizar
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df[features_cols])
   
    # K-Means 
    kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
    kmeans.fit(X_scaled)

    # PCA
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_scaled)
    
    plt.figure(figsize=(10, 8))

    # Pintar los puntos
    plt.scatter(X_pca[:, 0], X_pca[:, 1], c=kmeans.labels_, cmap='viridis', alpha=0.5)
    
    # Pintar los centros
    centros_pca = pca.transform(kmeans.cluster_centers_)
    plt.scatter(centros_pca[:, 0], centros_pca[:, 1], c='red', s=200, marker='X')
    
    plt.title("Visualización de Clusters de Usuarios")
    plt.show()
    print(f"📈 Gráfico guardado en {MODEL_PATH}/clusters_visualizacion.png")

    score = silhouette_score(X_scaled, kmeans.labels_)
    print(f"   Silhouette Score: {score:.4f}")

    # --- ETIQUETADO ---
    # Analizamos los centros de cada cluster para ponerle nombre
    centros = scaler.inverse_transform(kmeans.cluster_centers_)

    # Convertimos los centros a DataFrame para buscar máximos fácilmente
    df_centros = pd.DataFrame(centros, columns=features_cols)
    mapa_etiquetas = {}
    indices_asignados = []

    # 1. Encontrar al GAMER (El que tiene el máximo de ocio digital)
    idx_gamer = df_centros["ocio_digital_min"].idxmax()
    mapa_etiquetas[idx_gamer] = "GAMER"
    indices_asignados.append(idx_gamer)

    # 2. Encontrar al SENIOR (El de mayor edad, excluyendo los ya asignados)
    temp_df = df_centros.copy()
    temp_df.loc[indices_asignados, :] = -999 
    
    idx_senior = temp_df["edad"].idxmax()
    mapa_etiquetas[idx_senior] = "SENIOR"
    indices_asignados.append(idx_senior)

    # 3. Encontrar al DEPORTISTA (Máximo fitness_km restante)
    temp_df.loc[indices_asignados, :] = -999
    idx_deportista = temp_df["fitness_km"].idxmax()
    mapa_etiquetas[idx_deportista] = "DEPORTISTA"
    indices_asignados.append(idx_deportista)

    # 4. Encontrar al EJECUTIVO (Máximo vicios restante)
    temp_df.loc[indices_asignados, :] = -999
    idx_ejecutivo = temp_df["vicios_score"].idxmax()
    mapa_etiquetas[idx_ejecutivo] = "EJECUTIVO"
    indices_asignados.append(idx_ejecutivo)
    
    # 5. El que queda es ESTUDIANTE (o EQUILIBRADO)
    for i in range(5):
        if i not in indices_asignados:
            mapa_etiquetas[i] = "ESTUDIANTE"

    # 6. Generación de datos para frontend
    df["cluster"] = kmeans.labels_
    df["perfil"] = df["cluster"].map(mapa_etiquetas)

    #Calculamos el promedio real agrupado por perfil
    df_frontend = df.groupby("perfil")[frontend_cols].mean().reset_index()
    
    #Convertir a diccionario
    datos_agregados = df_frontend.to_dict(orient="records")

    # Guardar todo
    joblib.dump(kmeans, f"{MODEL_PATH}/kmeans_v2.pkl")
    joblib.dump(scaler, f"{MODEL_PATH}/scaler_v2.pkl")
    joblib.dump(features_cols, f"{MODEL_PATH}/cols_v2.pkl")
    joblib.dump(mapa_etiquetas, f"{MODEL_PATH}/labels_v2.pkl") # Guardamos el mapa
    joblib.dump(datos_agregados, f"{MODEL_PATH}/cluster_metrics_v2.pkl") #guardado de las métricas

    print("Modelo entrenado y etiquetas guardadas.")


# 4. PREDICCIÓN FINAL (API)

def predecir_perfil_usuario(db: Session, usuario_id: int):
    try:
        # Cargar recursos
        kmeans = joblib.load(f"{MODEL_PATH}/kmeans_v2.pkl")
        scaler = joblib.load(f"{MODEL_PATH}/scaler_v2.pkl")
        cols = joblib.load(f"{MODEL_PATH}/cols_v2.pkl")
        labels = joblib.load(f"{MODEL_PATH}/labels_v2.pkl")
        metrics_data = joblib.load(f"{MODEL_PATH}/cluster_metrics_v2.pkl")

       
        usuario = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
        if not usuario: return None

        # Calcular métricas
        metricas = extraer_metricas_usuario(usuario)

        # Predecir Cluster
        df_single = pd.DataFrame([metricas])

        X_scaled = scaler.transform(df_single[cols])

        cluster_id = int(kmeans.predict(X_scaled)[0])

        # Obtener nombre y consejo
        nombre_perfil = labels.get(cluster_id, "Desconocido")

        consejo = generar_consejo_salud(nombre_perfil)

        #Obtener media del grupo
        media_grupo = next((item for item in metrics_data if item["perfil"] == nombre_perfil), {})

        return {
            "grupo_id": cluster_id,
            "perfil_ia": nombre_perfil,
            "recomendacion": consejo,
            "metricas": metricas, # Útil para gráficas en frontend
            "comparativa_grupo": media_grupo
        }

    except FileNotFoundError:
        return {"error": "Modelo no entrenado"}
    except Exception as e:
        return {"error": f"Erro de predicción:{str(e)}"}

# Función para lectura de metrícas
def obtener_metricas_clusters():
    try:
        datos_agregados = joblib.load(f"{MODEL_PATH}/cluster_metrics_v2.pkl")
        return datos_agregados
    except FileNotFoundError:
        return None
    

if __name__ == "__main__":
    db = SessionLocal()
    try:
        entrenar_modelo(db)
        # Prueba rápida con el usuario 1
        print("\n🧪 PRUEBA DE PREDICCIÓN (Usuario 1):")
        resultado = predecir_perfil_usuario(db, 67)
        print(resultado)

    finally:
        db.close()