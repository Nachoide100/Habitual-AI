import joblib
import pandas as pd
import os

MODEL_PATH = "ml_models"

def auditar_medias():
    archivo_metricas = f"{MODEL_PATH}/cluster_metrics_v2.pkl"
    
    if not os.path.exists(archivo_metricas):
        print("❌ NO EXISTE EL ARCHIVO DE MÉTRICAS.")
        print("💡 Solución: Ejecuta el entrenamiento primero (POST /ml/entrenar)")
        return

    print("📂 Cargando archivo de promedios poblacionales...\n")
    datos = joblib.load(archivo_metricas)
    
    # Convertimos a DataFrame solo para verlo bonito en consola
    df = pd.DataFrame(datos)
    
    # Reordenamos columnas para leerlo mejor
    columnas_clave = ["perfil", "ocio_digital_min", "fitness_km", "sedentarismo_horas", "vicios_score", "lectura_paginas"]
    
    # Filtramos solo columnas que existan (por seguridad)
    cols_a_mostrar = [c for c in columnas_clave if c in df.columns]
    
    print("📊 MEDIAS CALCULADAS DE TUS 500 USUARIOS:")
    print("=" * 80)
    print(df[cols_a_mostrar].to_string(index=False))
    print("=" * 80)
    
    print("\n🧐 ANÁLISIS RÁPIDO:")
    for perfil in df['perfil'].unique():
        data_perfil = df[df['perfil'] == perfil].iloc[0]
        print(f"-> El {perfil} promedio hace {data_perfil.get('fitness_km', 0):.1f} km de deporte y juega {data_perfil.get('ocio_digital_min', 0):.1f} min a videojuegos.")

if __name__ == "__main__":
    auditar_medias()