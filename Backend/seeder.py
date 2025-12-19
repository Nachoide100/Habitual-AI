import random
from datetime import date, timedelta, datetime, time
from faker import Faker
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
from schemas import (
    CategoriaLibro, MomentoDia, TipoOcio, TipoSocial
)

# Configuración
fake = Faker('es_ES') 
NUM_USUARIOS = 500 
DIAS_HISTORIAL = 30 #
ZONAS_HORARIAS = [
    "Europe/Madrid", "Europe/London", "America/New_York", 
    "America/Mexico_City", "America/Bogota", "Asia/Tokyo", "Australia/Sydney"
]

#Función para asegurar la integridad de la base de datos
def limpiar_base_datos(db: Session):
    print("Limpiando base de datos antigua...")
    db.query(models.HabitoEntrada).delete()
    db.query(models.Habito).delete()
    db.query(models.Usuario).delete()
    db.commit()

#Función para crear los hábitos y usuarios
def crear_usuarios_y_habitos(db: Session):
    print(f"Creando {NUM_USUARIOS} usuarios con 5 perfiles...")
    
    usuarios_creados = [] #lista vacía donde almacenaremos los usuarios
    perfiles = ["DEPORTISTA", "ESTUDIANTE", "EJECUTIVO", "SENIOR", "GAMER"] #etiquetas para cada perfil

    for _ in range(NUM_USUARIOS): #bucle que asigna un perfil y sexo aleatorio a cada usuario
        perfil = random.choice(perfiles)
        genero = random.choice(["M", "F"]) 
        
        # Función auxiliar límite sup e inf (no valores negativos ni infinitos)
        def limit(val, min_v, max_v): 
            return max(min_v, min(max_v, val))

        # --- BASES BIOLÓGICAS ---
        # Definimos una base según el género, luego el perfil la modificará
        mu_altura = 176 if genero == "M" else 163
        mu_peso = 78 if genero == "M" else 63
        
        # --- DATOS DEMOGRÁFICOS ---
        
        if perfil == "DEPORTISTA":
            # Peso muscular (más alto que la media, pero sano)
            edad = int(limit(random.gauss(26, 5), 18, 40))
            peso = limit(random.gauss(mu_peso + 5, 5), 50, 110) 
            estilo = "deportista"
            
        elif perfil == "ESTUDIANTE":
            # Joven, con bastante variabilidad en peso
            edad = int(limit(random.gauss(21, 2), 18, 28))
            peso = limit(random.gauss(mu_peso - 2, 8), 45, 100)
            estilo = "estudiante"
            
        elif perfil == "EJECUTIVO":
            # Tendencia al sobrepeso por vida sedentaria y estrés
            edad = int(limit(random.gauss(42, 6), 30, 60))
            peso = limit(random.gauss(mu_peso + 10, 10), 60, 130)
            estilo = "oficina"
            
        elif perfil == "SENIOR":
            # Tendencia a perder altura y ganar/perder peso
            edad = int(limit(random.gauss(70, 5), 60, 85))
            mu_altura -= 2 # Se encogen un poco
            peso = limit(random.gauss(mu_peso, 8), 50, 100)
            estilo = "jubilado"
            
        elif perfil == "GAMER":
            # Extremos: Muy delgados o Muy pesados
            edad = int(limit(random.gauss(22, 4), 16, 35))
            if random.random() < 0.5: #probalidad del 50% de ser delgado o sobrepeso dentro de este perfil
                peso = limit(random.gauss(mu_peso - 10, 5), 45, 80) # Delgado
            else:
                peso = limit(random.gauss(mu_peso + 15, 10), 80, 140) # Sobrepeso
            estilo = "sedentario"

        # Generamos altura con variación normal
        altura = int(limit(random.gauss(mu_altura, 6), 145, 210))

        # Simulación de ABANDONO
        dia_abandono = None
        if random.random() < 0.10: 
            dia_abandono = random.randint(30, 100) 

        usuario = models.Usuario(
            nombre=fake.name(),
            edad=edad,
            genero=genero,
            peso=round(peso, 1),
            altura=altura, 
            estilo_vida=estilo,
            nivel_actividad="bajo" if perfil in ["GAMER", "EJECUTIVO", "ESTUDIANTE"] else "alto",
            timezone=random.choice(ZONAS_HORARIAS)
        )
        db.add(usuario)
        db.flush()

        # --- 2. ASIGNAR HÁBITOS (Igual que antes) ---
        mis_habitos = []
        
        # Básicos
        mis_habitos.append(models.Habito(nombre="Dormir", frecuencia="diario", tipo_habito="sueno", usuario_id=usuario.id))
        mis_habitos.append(models.Habito(nombre="Diario Emocional", frecuencia="diario", tipo_habito="estado_animo", usuario_id=usuario.id))

        if perfil == "DEPORTISTA":
            mis_habitos.append(models.Habito(nombre="Crossfit/Gym", frecuencia="diario", tipo_habito="fitness", usuario_id=usuario.id))
            mis_habitos.append(models.Habito(nombre="Dieta Macro", frecuencia="diario", tipo_habito="nutricion", usuario_id=usuario.id))
            mis_habitos.append(models.Habito(nombre="Meditación", frecuencia="diario", tipo_habito="meditacion", usuario_id=usuario.id))
            mis_habitos.append(models.Habito(nombre="Club Running", frecuencia="semanal", tipo_habito="actividad_social", usuario_id=usuario.id))

        elif perfil == "ESTUDIANTE":
            mis_habitos.append(models.Habito(nombre="Estudiar", frecuencia="diario", tipo_habito="habito_saludable", usuario_id=usuario.id)) # Sedentarismo
            mis_habitos.append(models.Habito(nombre="Salir de fiesta", frecuencia="semanal", tipo_habito="actividad_social", usuario_id=usuario.id)) 
            mis_habitos.append(models.Habito(nombre="Gaming", frecuencia="semanal", tipo_habito="actividad_ocio", usuario_id=usuario.id))
            mis_habitos.append(models.Habito(nombre="Lectura", frecuencia="semanal", tipo_habito="lectura", usuario_id=usuario.id))
            
        elif perfil == "EJECUTIVO":
            mis_habitos.append(models.Habito(nombre="Television", frecuencia="diario", tipo_habito="actividad_ocio", usuario_id=usuario.id))
            mis_habitos.append(models.Habito(nombre="Comida Oficina", frecuencia="semanal", tipo_habito="actividad_social", usuario_id=usuario.id)) 
            mis_habitos.append(models.Habito(nombre="Trabajar", frecuencia="diario", tipo_habito="habito_saludable", usuario_id=usuario.id)) 
            mis_habitos.append(models.Habito(nombre="Cena rápida", frecuencia="diario", tipo_habito="nutricion", usuario_id=usuario.id)) 

        elif perfil == "SENIOR":
            mis_habitos.append(models.Habito(nombre="Paseo Matutino", frecuencia="diario", tipo_habito="fitness", usuario_id=usuario.id))
            mis_habitos.append(models.Habito(nombre="Prensa/Libros", frecuencia="diario", tipo_habito="lectura", usuario_id=usuario.id))
            mis_habitos.append(models.Habito(nombre="Dieta Mediterránea", frecuencia="diario", tipo_habito="nutricion", usuario_id=usuario.id))
            mis_habitos.append(models.Habito(nombre="Club Social", frecuencia="semanal", tipo_habito="actividad_social", usuario_id=usuario.id))

        elif perfil == "GAMER":
            mis_habitos.append(models.Habito(nombre="Cyber", frecuencia="semanal", tipo_habito="actividad_social", usuario_id=usuario.id))
            mis_habitos.append(models.Habito(nombre="Junk Food", frecuencia="diario", tipo_habito="nutricion", usuario_id=usuario.id))
            mis_habitos.append(models.Habito(nombre="Videojuegos", frecuencia="diario", tipo_habito="actividad_ocio", usuario_id=usuario.id))
            mis_habitos.append(models.Habito(nombre="Lectura Cómics", frecuencia="diario", tipo_habito="lectura", usuario_id=usuario.id))

        db.add_all(mis_habitos)
        db.flush()
        
        # Preparamos el estado para la generación de historia
        habitos_con_estado = [{"obj": h, "racha": 0} for h in mis_habitos]
        
        # --- ADN  ---
        # Definimos una "normalidad" para cada perfil (sino todos tendrán la misma media)
         
        adn = {
            "sueno_media": random.gauss(7.5, 0.5) if perfil not in ["EJECUTIVO", "GAMER", "ESTUDIANTE"] else random.gauss(6.0, 0.8),
            "fitness_media": random.gauss(60, 15) if perfil in ["DEPORTISTA", "SENIOR"] else random.gauss(20, 10),
            "vicios_media": random.gauss(5, 2) if perfil in ["GAMER", "EJECUTIVO", "ESTUDIANTE"] else random.gauss(0.5, 0.5)
        }

        usuarios_creados.append({
            "perfil": perfil, 
            "habitos_info": habitos_con_estado,
            "abandona_en_dia": dia_abandono,
            "adn": adn # Guardamos su ADN para usarlo en el bucle diario
        })

    db.commit()
    return usuarios_creados

def generar_historial(db: Session, datos_usuarios):
    print(f"Simulando {DIAS_HISTORIAL} días...")
    
    buffer_entradas = [] #lista donde almacenar las entradas  

    hoy = date.today()
    for i in range(DIAS_HISTORIAL, 0, -1): #bucle para recorrer los días de la simulación
        fecha_simulada = hoy - timedelta(days=i)
        es_finde = fecha_simulada.weekday() >= 5 #comprobación numeríca del finde
        dia_numero = DIAS_HISTORIAL - i  #contador en sentido ascendente

        for user_data in datos_usuarios: #bucle que recorre cada usuario
            if user_data["abandona_en_dia"] and dia_numero > user_data["abandona_en_dia"]: continue #check de abandono
            if random.random() < 0.03: continue #"ruido"

            perfil = user_data["perfil"] #asginacion de caracterísitcas específicas
            adn = user_data["adn"] 
            
            for h_info in user_data["habitos_info"]:  #bucle para recorrer el habitos_con_estado
                habito = h_info["obj"]
                
                # Probabilidad base
                prob = 0.5 + (0.15 if h_info["racha"] > 0 else 0) #probabilidad base + racha
                if es_finde and perfil in ["ESTUDIANTE", "GAMER"]: prob += 0.2 #mas disponibilidad findes de semama
                if es_finde and perfil == "EJECUTIVO": prob += 0.25
                
                if random.random() < prob: #generación de probabilidad para determinar hábito cumplido
                    h_info["racha"] += 1


                    valor = {}
                    
                    # --- CONDICIÓN DE HÁBITOS---
                    
                    if habito.tipo_habito == "sueno":
                        # Usamos su media personal + variación diaria
                        horas = random.gauss(adn["sueno_media"], 1.2) 
                        if es_finde: horas += random.uniform(0.5, 2.0) #la gente en general duerme más los findes
                        
                        #Límites para horas de sueño (nadie duerme 24 horas)
                        horas = max(3.0, min(14.0, horas))
                        
                        #Concionamiento de calidad
                        calidad = int(max(1, min(10, (horas/1.1) + random.uniform(-2, 2)))), #calidad base + "ruido"

                        #Condicionamiento por perfil
                        se_levanta_temprano = (perfil not in ["GAMER"])

                        if perfil in ["ESTUDIANTE", "EJECUTIVO"] and es_finde:
                            se_levanta_temprano = False

                        #JSON final 
                        valor = {
                            "horas": round(horas, 1),
                            "calidad": calidad,  
                            "madrugar": se_levanta_temprano
                        }

                    elif habito.tipo_habito == "fitness":
                       #1. Detectar tipo de deportista
                       es_gym = "Gym" in habito.nombre
                       es_running = "Running" in habito.nombre
                       es_paseo = "Paseo" in habito.nombre #Para seniors

                       #2. Cáculo de la duración del ejercicio
                       media_duracion = adn["fitness_media"] #basándonos en el adn generado antes
                       duracion = int(random.gauss(media_duracion, 15))

                       #3. Manejar findes de semana (más tiempo para todos para hacer ejecicio)
                       if es_finde:
                            if perfil in ["DEPORTISTA", "SENIOR"]:
                               duracion += 30 #los senior andan mucho más y los deportistas entrenan más duro
                            else:
                                duracion += 15 #otros grupos disponen de más tiempo pero no están acostumbrados
                        
                       #Límites superior e inferior
                       duracion = max(10, min(180, duracion))
                       
                       #CÁLCULO DE DISTANCIA E INTENSIDAD SEGUN TIPO DE EJ
                       #Valores por defecto de las variables
                       distancia = 0.0
                       intensidad = 2
                       tipo_ej = "cardio"

                        #Modificación de las variables según el tipo de ejercicio
                       if es_gym:
                            # Gym = Intensidad alta, 0 km (o muy poco de cinta)
                            distancia = 0.0
                            intensidad = random.gauss(4, 0.5)
                            tipo_ej = "fuerza"
                        
                       elif es_running:
                            # Running = Intensidad alta, Distancia basada en ritmo (ej: 5 min/km)
                            ritmo = random.uniform(4.5, 6.0) # min/km
                            distancia = round(duracion / ritmo, 2)
                            intensidad = random.gauss(2.5, 2) #hay varios tipos de running
                            tipo_ej = "running"
                            
                       elif es_paseo:
                            # Paseo = Intensidad baja, Distancia basada en ritmo lento (ej: 12 min/km)
                            ritmo = random.uniform(10.0, 14.0) 
                            distancia = round(duracion / ritmo, 2)
                            intensidad = random.gauss(1.5, 0.75)
                            tipo_ej = "caminar" 

                       #Almacenamiento de los valores en el JSON
                       valor = {
                            "duracion_minutos": duracion,
                            "distancia_km": distancia,
                            "intensidad": intensidad,
                            "tipo_ejercicio": tipo_ej
                        } 
                        

                    elif habito.tipo_habito == "nutricion": #detección de comida basura
                        es_junk = "Junk" in habito.nombre or "rápida" in habito.nombre or "basura" in habito.nombre
                        
                        # Medias base según perfil
                        mu_fruta = 3.0 if perfil ==  "DEPORTISTA" else 1.0
                        mu_proteina = 4.0 if perfil == "DEPORTISTA" else 1.5
                        mu_hidratos = 3.5 if perfil == "DEPORTISTA" else 2 #suele ser una comida facil de cocinar
                        
                        if perfil in ["GAMER", "EJECUTIVO"]:
                            mu_fruta = 0.5 # Comen poca fruta y verdura
                            mu_verdura = 0.5

                        if perfil in ["SENIOR"]:
                            es_junk = False #tienen que controlar tema de tensión, etc.
                        
                        agua = random.gauss(2.0, 0.8) #mucha variabilidad en la ingesta de agua
                        if perfil == "DEPORTISTA": agua += 1.0  # + deporte, + agua
                        
                        valor = {
                            "agua_litros": round(max(0.5, min(5.0, agua)), 1),
                            "cheat_meal": es_junk or (es_finde and random.random() < 0.4), #al ser finde hasta el deportista puede ir a comer por ahí
                            "fruta": int(max(0, random.gauss(mu_fruta, 1.0))),
                            "verdura": int(max(0, random.gauss(mu_fruta, 1.0))),
                            "proteina_animal": int(max(0, random.gauss(mu_proteina, 1.0))),
                            "hidratos": int(max(1, random.gauss(mu_hidratos, 1.5)))
                        }

                    elif habito.tipo_habito == "habito_saludable":
                        # CÁLCULO DE SEDENTARISMO
                        # Base general para todos (trabajo/estudio estándar)
                        horas_base = random.gauss(6, 1.5) 
                        
                        # Bonus por perfil
                        if perfil == "GAMER": 
                            horas_base += 5.0 
                        elif perfil == "EJECUTIVO": 
                            horas_base += 4.0 
                        elif perfil == "ESTUDIANTE": 
                            horas_base += 3.0 
                        elif perfil == "DEPORTISTA":
                            horas_base -= 1.0 
                            
                        # Bonus Fin de Semana
                        if es_finde:
                            if perfil == "GAMER": horas_base += 2.0 
                            else: horas_base -= 2.0 

                        # Limites inferior y superior
                        sedentarismo = int(max(2, min(16, horas_base)))

                        # CÁLCULO DE VICIOS
                        alcohol = 0
                        tabaco = 0
                        
                        # Alcohol
                        if perfil == "ESTUDIANTE" and es_finde:
                            # Beben mucho, pero solo el finde
                            alcohol = int(max(0, random.gauss(adn["vicios_media"] + 2, 3)))
                        
                        elif perfil == "EJECUTIVO":
                            # Beben constante (comidas negocio) + extra finde
                            base_alcohol = adn["vicios_media"]
                            if es_finde: base_alcohol += 2
                            alcohol = int(max(0, random.gauss(base_alcohol, 1.5)))
                            
                        elif perfil == "GAMER" and es_finde:
                            # Beben ocasionalmente
                            alcohol = int(max(0, random.gauss(1, 1)))

                        # Tabaco
                        prob_fumar = 0.0
                        if perfil == "EJECUTIVO": prob_fumar = 0.4
                        elif perfil in ["ESTUDIANTE", "SENIOR"]: prob_fumar = 0.15
                        
                        if random.random() < prob_fumar:
                            # Si fuma, fuma según su media de vicios
                            tabaco = int(max(1, random.gauss(adn["vicios_media"], 3)))

                        valor = {
                            "sedentarismo": sedentarismo,
                            "alcohol": alcohol,
                            "tabaco": tabaco
                        }

                    elif habito.tipo_habito == "actividad_social":
                        # 1. Detectar subtipos específicos por nombre
                        es_fiesta = "fiesta" in habito.nombre      
                        es_trabajo = "Oficina" in habito.nombre    
                        es_cyber = "Cyber" in habito.nombre        
                        
                        # 2. Duración y Momento según el subtipo
                        if es_fiesta:
                            duracion = int(random.gauss(240, 60)) # Media 4 horas
                            momento = MomentoDia.NOCHE.value
                            tipo = TipoSocial.AMIGOS.value
                            
                        elif es_cyber:
                            duracion = int(random.gauss(180, 45)) # Media 3 horas
                            momento = MomentoDia.NOCHE.value
                            tipo = TipoSocial.AMIGOS.value
                            
                        elif es_trabajo:
                            duracion = int(random.gauss(75, 15)) 
                            momento = MomentoDia.MANANA.value # Mediodía 
                            tipo = TipoSocial.COMPAÑEROS_TRABAJO.value
                            
                        else:
                            # Otros, club social o quedada por la tarde a tomar algo
                            duracion = int(random.gauss(90, 30)) 
                            momento = MomentoDia.TARDE.value 
                            tipo = TipoSocial.AMIGOS.value 

                        # 3. Bonus de Fin de Semana (La gente socializa más tiempo el finde)
                        if es_finde and not es_trabajo:
                            duracion += 60

                        # Límite superior e inferior
                        duracion = max(30, min(480, duracion))

                        #Creación del diccionario JSON
                        valor = {
                            "minutos": duracion,
                            "momento": momento,
                            "tipo_social": tipo
                        }

                    elif habito.tipo_habito == "actividad_ocio":
                        # 1. CÁLCULO DE DURACIÓN (Base)
                        # Gamers juegan mucho, los demás suelen tener menos tiempo
                        media_duracion = 120 if perfil in ["GAMER", "SENIOR"] else 60
                        
                        duracion = int(random.gauss(media_duracion, 30))
                        
                        # Bonus Finde
                        if es_finde: 
                            duracion += 60
                            if perfil == "GAMER": duracion += 90 # Maratón

                        #Límite superior e inferior
                        duracion = max(20, min(600, duracion))

                        # 2. SELECCIÓN DEL TIPO DE OCIO
                        # Inicializar las variables
                        tipo = TipoOcio.TELEVISION.value
                        momento = MomentoDia.NOCHE.value

                        if perfil == "GAMER":
                            tipo = TipoOcio.VIDEOJUEGOS.value
                            momento = MomentoDia.NOCHE.value # Juegan hasta tarde
                        
                        elif perfil == "EJECUTIVO":
                            tipo = TipoOcio.TELEVISION.value 
                            momento = MomentoDia.NOCHE.value # Después de trabajar
                            
                        elif perfil == "ESTUDIANTE":
                            # El estudiante varía más
                            dado_ocio = random.random()
                            if dado_ocio < 0.4:
                                tipo = TipoOcio.DIBUJO_ARTE.value
                                momento = MomentoDia.TARDE.value # Tienen tardes libres
                            elif dado_ocio < 0.5:
                                tipo = TipoOcio.VIDEOJUEGOS.value
                                momento = MomentoDia.NOCHE.value
                            elif dado_ocio < 0.25:
                                tipo = TipoOcio.JUEGOMESA.value
                                momento = MomentoDia.TARDE.value
                        
                        elif perfil == "SENIOR":
                            # Seniors ven TV o juegan a cartas/mesa
                            if random.random() < 0.6:
                                tipo = TipoOcio.TELEVISION.value
                                momento = MomentoDia.NOCHE.value
                            else:
                                tipo = TipoOcio.JUEGOMESA.value # Dominó, cartas...
                                momento = MomentoDia.TARDE.value

                        # Si es fin de semana y la duración es muy larga, asumimos que empezaron tarde
                        if es_finde and duracion > 180:
                            momento = MomentoDia.TARDE.value

                        valor = {
                            "minutos": duracion,
                            "momento": momento,
                            "tipo_ocio": tipo
                        }

                    elif habito.tipo_habito == "lectura":
                        es_comics = "Cómics" in habito.nombre
                        es_estudio = "Estudiar" in habito.nombre or "Prensa" in habito.nombre
                        
                        # 1. PÁGINAS (Media)
                        if es_comics:
                            media_pag = 40 # Cómics se leen rápido y muchos
                            desviacion = 15
                        elif es_estudio:
                            media_pag = 15 # Estudiar o el periódico es denso, avanzas lento
                            desviacion = 5
                        else:
                            media_pag = 25 # Novela estándar
                            desviacion = 10
                        
                        paginas = int(max(5, random.gauss(media_pag, desviacion)))
                        
                        # Día que te enganches al libro 
                        if not es_estudio and random.random() < 0.05: 
                            paginas *= 3
                        
                        # 2. TIEMPO (Minutos por página)
                        if es_comics:
                            # Un cómic se lee muy rápido (0.5 a 1 min por página)
                            velocidad = random.uniform(0.5, 1.0)
                        elif es_estudio:
                            # Estudiar es muy lento (3 a 5 min por página)
                            velocidad = random.uniform(3.0, 5.0)
                        else:
                            # Lectura normal 
                            velocidad = random.uniform(1, 2)
                            
                        minutos = int(paginas * velocidad)

                        # 3. CATEGORÍA
                        categoria = CategoriaLibro.NO_FICCION.value
                        if es_comics or (perfil == "SENIOR" and random.random() < 0.25): 
                            categoria = CategoriaLibro.FICCION.value

                        valor = {
                            "paginas": paginas,
                            "minutos": minutos,
                            "categoria": categoria
                        }
                    
                    elif habito.tipo_habito == "meditacion":
                        # 1. DURACIÓN 
                        # El deportista y el senior suele dedicar más tiempo
                        media_min = 30 if perfil in ["DEPORTISTA", "SENIOR"] else 15
                        if "Express" in habito.nombre: media_min = 10 # Caso de tener muy poco tiempo
        
                        minutos = int(max(5, random.gauss(media_min, 10)))
                        
                        # 2. MOMENTO DEL DÍA
                        # Por defecto mañana, pero puede ser para dormir
                        momento = MomentoDia.MANANA.value
                        if perfil == "EJECUTIVO" or "Dormir" in habito.nombre:
                            momento = MomentoDia.NOCHE.value

                        # 3. ESTRÉS PREVIO (Basado en el perfil)
                        base_estres = 5 # Normal
                        if perfil == "EJECUTIVO": base_estres = 8.5 # Muy estresado
                        elif perfil in ["DEPORTISTA", "SENIOR"]: base_estres = 3.5 #el deporte y la vida de jubilado
                        elif perfil == "ESTUDIANTE" and es_finde: base_estres = 4.0 # Relajado el finde
                        
                        estres_antes = int(max(1, min(10, random.gauss(base_estres, 1.5))))

                        # 4. CÁLCULO DE ESTRÉS POSTERIOR 
                        # Fórmula: Por cada 10 minutos, bajas 1 punto de estrés 
                        eficacia = 0.15 if perfil == "DEPORTISTA" else 0.10
                        
                        reduccion = int(minutos * eficacia) 
                        
                        # Añadimos un poco de ruido 
                        reduccion += random.randint(-1, 1)
                        
                        # Calculamos y limitamos 
                        estres_despues = max(1, estres_antes - reduccion)

                        valor = {
                            "minutos": minutos,
                            "momento": momento,
                            "estres_antes": estres_antes,
                            "estres_despues": estres_despues
                        }
                        
                    elif habito.tipo_habito == "estado_animo":
                        # 1. BASE SEGÚN PERFIL 
                        media_animo = 7.0 # Persona promedio
                        desviacion = 1.5  # Estabilidad emocional normal
                        
                        if perfil == "EJECUTIVO":
                            media_animo = 5.5 
                            desviacion = 2.0  
                        elif perfil == "DEPORTISTA":
                            media_animo = 8.0 
                            desviacion = 1.0  
                        elif perfil == "ESTUDIANTE":
                            media_animo = 6.5 
                        elif perfil == "SENIOR":
                            media_animo = 6
                            desviacion = 3  #días que se pueden encontrar muy mal por temas de salud
                        
                        # 2. EFECTO FIN DE SEMANA
                        if es_finde:
                            media_animo += 1.5 # Todo el mundo es más feliz el finde
                        
                        # 3. GENERACIÓN DEL VALOR Y LÍMITES
                        puntuacion = int(max(1, min(10, random.gauss(media_animo, desviacion))))
                        
                        # 4. NIVEL DE ENERGÍA (Correlacionado con el ánimo)
                        # Usamos la puntuación como base y añadimos variación.
                        energia = int(max(1, min(10, random.gauss(puntuacion, 1.5))))
                        
                        # 5. GENERACIÓN DE NOTAS
                        notas = ""
                        if random.random() < 0.3: # Solo el 30% de los días escriben algo
                            if puntuacion >= 8:
                                notas = random.choice(["Día productivo", "Genial", "Motivado", "Buen entreno"])
                            elif puntuacion <= 4:
                                notas = random.choice(["Estresado", "Cansado", "Mal día", "Agobio"])
                            else:
                                notas = random.choice(["Normal", "Rutina", "Ok"])

                        valor = {
                            "puntuacion_dia": puntuacion, 
                            "nivel_energia": energia, 
                            "notas": notas
                        }

                    # Guardar
                    if valor:
                        entrada = models.HabitoEntrada(
                            fecha=fecha_simulada,
                            valor=valor,
                            habito_id=habito.id,
                            creado_a=datetime.combine(fecha_simulada, datetime.min.time())
                        )
                        buffer_entradas.append(entrada)
                else:
                    h_info["racha"] = 0

        # Batch
        if len(buffer_entradas) > 5000:
            db.add_all(buffer_entradas)
            db.commit()
            buffer_entradas = []

    if buffer_entradas:
        db.add_all(buffer_entradas)
        db.commit()

if __name__ == "__main__":
    db = SessionLocal()
    try:
        models.Base.metadata.create_all(bind=engine)
        limpiar_base_datos(db)
        datos = crear_usuarios_y_habitos(db)
        generar_historial(db, datos)
        print("SEEDER generado.")
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()