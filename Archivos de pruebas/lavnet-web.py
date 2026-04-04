import os
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta, timezone
import locale
from astral import LocationInfo
from astral.sun import sun
import pytz
import time
import subprocess
import threading
from matplotlib.animation import FuncAnimation
import matplotlib.gridspec as gridspec
import requests
import json
from bs4 import BeautifulSoup

# Establecer locale a español
try:
    locale.setlocale(locale.LC_TIME, 'es_ES.utf8')
except:
    try:
        locale.setlocale(locale.LC_TIME, 'es_MX.utf8')
    except:
        print("Locale español no disponible, usando default")

# Configuración de las estaciones
ESTACIONES = {
    'NAA': {
        'nombre': 'NAA Cutler, Maine',
        'location': LocationInfo("NAA", "USA", "America/Halifax", 44.6333, -67.2667),
        'color_amp': 'blue',
        'color_fase': 'red',
        'ip': '192.168.1.67',
        'remote_path': '/home/radzac/Datos_SID/mon/NAA'
    },
    'NDK': {
        'nombre': 'NDK LaMoure, Dakota Norte',
        'location': LocationInfo("NDK", "USA", "America/Chicago", 46.365, -98.335),
        'color_amp': 'blue',
        'color_fase': 'red',
        'ip': '192.168.1.67',
        'remote_path': '/home/radzac/Datos_SID/mon/NDK'
    },
    'NLK': {
        'nombre': 'NLK Jim Creek, Washington',
        'location': LocationInfo("NLK", "USA", "America/Los_Angeles", 48.204, -121.919),
        'color_amp': 'blue',
        'color_fase': 'red',
        'ip': '192.168.1.67',
        'remote_path': '/home/radzac/Datos_SID/mon/NLK'
    },
    'NAU': {
        'nombre': 'NAU Aguada, Puerto Rico',
        'location': LocationInfo("NAU", "Puerto Rico", "America/Puerto_Rico", 18.415, -67.154),
        'color_amp': 'blue',
        'color_fase': 'red',
        'ip': '192.168.1.67',
        'remote_path': '/home/radzac/Datos_SID/mon/NAU'
    },
    'NPM': {
        'nombre': 'NPM Lualualei, Hawaii',
        'location': LocationInfo("NPM", "USA", "Pacific/Honolulu", 21.423, -158.154),
        'color_amp': 'blue',
        'color_fase': 'red',
        'ip': '192.168.1.67',
        'remote_path': '/home/radzac/Datos_SID/mon/NPM'
    },
    'NWC': {
        'nombre': 'NWC North West Cape, Australia',
        'location': LocationInfo("NWC", "Australia", "Australia/Perth", -21.816, 114.165),
        'color_amp': 'blue',
        'color_fase': 'red',
        'ip': '192.168.1.67',
        'remote_path': '/home/radzac/Datos_SID/mon/NWC'
    }
}

# Directorios locales
BASE_DATA_DIR = "/home/ivan/vlfrx-tools-0.9p/Datos_Sid"
BASE_OUTPUT_DIR = "/home/ivan/Documentos/LAVNet-ZAC"
USER = "radzac"

# Configuración de fulguraciones solares
FLARE_DATA = {
    'last_update': None,
    'events': []
}

# Configuración de ventana temporal (variable global)
VENTANA_TIEMPO = 24  # horas por defecto
OPCIONES_TIEMPO = [6, 12, 24, 48, 72]  # horas disponibles

# CORRECCIÓN PARA DESFASE DE 30 MINUTOS
DESFASE_CORRECCION = timedelta(minutes=30)  # Ajuste para compensar el desfase

# CONFIGURACIÓN DE ACTUALIZACIÓN (5 MINUTOS PARA TODO)
INTERVALO_ACTUALIZACION_COMPLETA = 300  # 5 minutos en segundos

def seleccionar_ventana_temporal():
    """Permite al usuario seleccionar la ventana temporal"""
    global VENTANA_TIEMPO
    
    print("\n⏰ SELECCIÓN DE VENTANA TEMPORAL")
    print("=" * 40)
    for i, horas in enumerate(OPCIONES_TIEMPO, 1):
        print(f"{i}. Últimas {horas} horas")
    
    try:
        seleccion = input(f"\nSelecciona una opción (1-{len(OPCIONES_TIEMPO)}) [Por defecto: {VENTANA_TIEMPO}h]: ").strip()
        
        if seleccion:
            opcion = int(seleccion) - 1
            if 0 <= opcion < len(OPCIONES_TIEMPO):
                VENTANA_TIEMPO = OPCIONES_TIEMPO[opcion]
                print(f"✅ Ventana temporal configurada: {VENTANA_TIEMPO} horas")
            else:
                print(f"⚠ Opción inválida. Usando {VENTANA_TIEMPO} horas por defecto")
        else:
            print(f"✅ Usando {VENTANA_TIEMPO} horas por defecto")
            
    except ValueError:
        print(f"⚠ Entrada inválida. Usando {VENTANA_TIEMPO} horas por defecto")
    
    return VENTANA_TIEMPO

def obtener_fulguraciones_solares():
    """Obtiene datos de fulguraciones solares de NOAA"""
    try:
        print("🔆 Obteniendo datos de fulguraciones solares...")
        
        # URL de datos de NOAA GOES X-ray
        url = "https://services.swpc.noaa.gov/json/goes/primary/xrays-7-day.json"
        
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            
            # Procesar eventos significativos (M y X class)
            eventos_significativos = []
            
            for item in data:
                # Verificar que tenga los campos necesarios
                if all(key in item for key in ['time_tag', 'flux', 'energy']):
                    try:
                        # Manejar correctamente el timestamp
                        if isinstance(item['time_tag'], str):
                            # Si es string, convertir a datetime
                            timestamp = datetime.fromisoformat(item['time_tag'].replace('Z', '+00:00'))
                        else:
                            # Si es numérico (timestamp en ms)
                            timestamp = datetime.fromtimestamp(item['time_tag'] / 1000, tz=timezone.utc)
                        
                        # Convertir flux a float si es string
                        flux_val = float(item['flux'])
                        energy = item['energy']
                        
                        # Solo eventos significativos (Clase M1.0 o superior)
                        if energy == '0.05-0.4nm' and flux_val >= 1e-5:  # M1.0 o superior
                            clase_fulg = clasificar_fulguracion(flux_val)
                            
                            eventos_significativos.append({
                                'timestamp': timestamp,
                                'flux': flux_val,
                                'energy': energy,
                                'class': clase_fulg
                            })
                            
                    except (ValueError, TypeError) as e:
                        print(f"    ⚠ Error procesando item: {e}")
                        continue
            
            FLARE_DATA['events'] = eventos_significativos
            FLARE_DATA['last_update'] = datetime.now(timezone.utc)
            print(f"✅ {len(eventos_significativos)} eventos solares significativos encontrados")
            
            # Mostrar eventos encontrados
            for evento in eventos_significativos:
                print(f"    ⭐ {evento['timestamp'].strftime('%H:%M UT')} - Clase {evento['class']}")
                
            return eventos_significativos
            
        else:
            print(f"❌ Error HTTP: {response.status_code}")
            return generar_datos_solares_ejemplo()
            
    except Exception as e:
        print(f"❌ Error obteniendo datos solares: {e}")
        print("    Usando datos de ejemplo...")
        return generar_datos_solares_ejemplo()

def clasificar_fulguracion(flux):
    """Clasifica la fulguración solar según el flujo de rayos X"""
    flux = float(flux)
    
    if flux < 1e-7:
        return "A"
    elif flux < 1e-6:
        return "B"
    elif flux < 1e-5:
        # Clase C con valor específico (ej: C5.4)
        valor_c = flux / 1e-6
        return f"C{valor_c:.1f}"
    elif flux < 1e-3:
        # Clase M con valor específico (ej: M5.2)
        valor_m = flux / 1e-5
        return f"M{valor_m:.1f}"
    else:
        # Clase X con valor específico
        valor_x = flux / 1e-4
        return f"X{valor_x:.1f}"

def generar_datos_solares_ejemplo():
    """Genera datos de ejemplo para desarrollo"""
    ahora = datetime.now(timezone.utc)
    eventos = []
    
    # Ejemplo de evento M5.2 (como en tu código original)
    eventos.append({
        'timestamp': datetime(ahora.year, ahora.month, ahora.day, 18, 5, 0, tzinfo=timezone.utc),
        'flux': 5.2e-5,  # M5.2
        'energy': '0.05-0.4nm',
        'class': 'M5.2'
    })
    
    # Ejemplo de evento C2.1
    eventos.append({
        'timestamp': datetime(ahora.year, ahora.month, ahora.day, 12, 30, 0, tzinfo=timezone.utc),
        'flux': 2.1e-6,  # C2.1
        'energy': '0.05-0.4nm',
        'class': 'C2.1'
    })
    
    # Ejemplo de evento X1.5
    eventos.append({
        'timestamp': datetime(ahora.year, ahora.month, ahora.day, 15, 45, 0, tzinfo=timezone.utc),
        'flux': 1.5e-4,  # X1.5
        'energy': '0.05-0.4nm',
        'class': 'X1.5'
    })
    
    FLARE_DATA['events'] = eventos
    FLARE_DATA['last_update'] = ahora
    
    print("📋 Usando datos de ejemplo de fulguraciones:")
    for evento in eventos:
        print(f"    ⭐ {evento['timestamp'].strftime('%H:%M UT')} - Clase {evento['class']}")
    
    return eventos

def obtener_eventos_solares_ventana(horas=24):
    """Obtiene eventos solares de la ventana temporal seleccionada"""
    ahora = datetime.now(timezone.utc)
    
    # Actualizar datos cada ciclo completo (5 minutos)
    if (FLARE_DATA['last_update'] is None or 
        (ahora - FLARE_DATA['last_update']).total_seconds() > INTERVALO_ACTUALIZACION_COMPLETA):
        obtener_fulguraciones_solares()
    
    # Filtrar eventos de la ventana temporal
    inicio_ventana = ahora - timedelta(hours=horas)
    eventos_ventana = [evento for evento in FLARE_DATA['events'] 
                      if evento['timestamp'] >= inicio_ventana]
    
    return eventos_ventana

def obtener_erupciones_mas_intensas():
    """Obtiene las erupciones más intensas de cada categoría (C, M, X)"""
    eventos_24h = obtener_eventos_solares_ventana(24)
    
    if not eventos_24h:
        return []
    
    # Encontrar la más intensa de cada clase
    max_c = None
    max_m = None
    max_x = None
    
    for evento in eventos_24h:
        clase = evento['class'][0]  # Primera letra (C, M, X)
        flux = evento['flux']
        
        if clase == 'C':
            if max_c is None or flux > max_c['flux']:
                max_c = evento
        elif clase == 'M':
            if max_m is None or flux > max_m['flux']:
                max_m = evento
        elif clase == 'X':
            if max_x is None or flux > max_x['flux']:
                max_x = evento
    
    # Retornar solo las más intensas (si existen)
    erupciones_intensas = []
    if max_c:
        erupciones_intensas.append(max_c)
    if max_m:
        erupciones_intensas.append(max_m)
    if max_x:
        erupciones_intensas.append(max_x)
    
    return erupciones_intensas

def descargar_datos_estacion(estacion_codigo):
    """Descarga los datos usando los comandos exactos de SCP"""
    estacion = ESTACIONES[estacion_codigo]
    
    # Crear directorio local
    local_dir = f"{BASE_DATA_DIR}/mon/{estacion_codigo}"
    os.makedirs(local_dir, exist_ok=True)
    
    try:
        # USAR COMANDOS EXACTOS de SCP
        if estacion_codigo == 'NAA':
            cmd = f"scp {USER}@{estacion['ip']}:/home/radzac/Datos_SID/mon/NAA/2510* {local_dir}/"
        elif estacion_codigo == 'NDK':
            cmd = f"scp {USER}@{estacion['ip']}:/home/radzac/Datos_SID/mon/NDK/25101* {local_dir}/"
        elif estacion_codigo == 'NLK':
            cmd = f"scp {USER}@{estacion['ip']}:/home/radzac/Datos_SID/mon/NLK/2510* {local_dir}/"
        elif estacion_codigo == 'NAU':
            cmd = f"scp {USER}@{estacion['ip']}:/home/radzac/Datos_SID/mon/NAU/2510* {local_dir}/"
        elif estacion_codigo == 'NPM':
            cmd = f"scp {USER}@{estacion['ip']}:/home/radzac/Datos_SID/mon/NPM/2510* {local_dir}/"
        elif estacion_codigo == 'NWC':
            cmd = f"scp {USER}@{estacion['ip']}:/home/radzac/Datos_SID/mon/NWC/2510* {local_dir}/"
        
        print(f"📥 Descargando {estacion_codigo}...")
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            archivos = [f for f in os.listdir(local_dir) if f.startswith('2510')]
            print(f"✅ {estacion_codigo}: {len(archivos)} archivos descargados")
            return True
        else:
            print(f"❌ Error {estacion_codigo}: {result.stderr.strip()}")
            return False
            
    except Exception as e:
        print(f"❌ Error {estacion_codigo}: {e}")
        return False

def procesar_con_vtsidex(estacion_codigo):
    """Procesa datos usando vtsidex con parámetros exactos"""
    ahora = datetime.now()
    
    # Crear directorio de salida
    output_dir = f"{BASE_OUTPUT_DIR}/{ahora.year}/{estacion_codigo}/{ahora.month:02d}"
    os.makedirs(output_dir, exist_ok=True)
    
    # Configurar el mes completo
    start_date = datetime(ahora.year, ahora.month, 1)
    if ahora.month == 12:
        end_date = datetime(ahora.year + 1, 1, 1) - timedelta(days=1)
    else:
        end_date = datetime(ahora.year, ahora.month + 1, 1) - timedelta(days=1)
    
    archivos_procesados = 0
    
    # Iterar sobre las fechas en el rango
    current_date = start_date
    while current_date <= end_date:
        formatted_date = current_date.strftime("%Y-%m-%d")
        
        # Generar el rango horario EXACTO
        start_time = f"{formatted_date}_00"
        end_time = f"{formatted_date}_24"
        
        # Generar nombre del archivo de salida EXACTO
        output_filename = current_date.strftime("%d-%m-%Y.txt")
        output_path = os.path.join(output_dir, output_filename)
        
        # Comando vtsidex EXACTO
        command = f"vtsidex -m {estacion_codigo} -a15 -h360 -T{start_time},{end_time} {BASE_DATA_DIR} > {output_path}"
        
        try:
            print(f"  🔄 Procesando {formatted_date}...")
            result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                if os.path.exists(output_path) and os.path.getsize(output_path) > 100:
                    with open(output_path, 'r') as f:
                        line_count = len(f.readlines())
                    print(f"  ✅ {formatted_date}: {line_count} líneas")
                    archivos_procesados += 1
                else:
                    print(f"  ⚠ {formatted_date}: archivo vacío")
            else:
                print(f"  ❌ Error vtsidex: {result.stderr.strip()}")
                
        except Exception as e:
            print(f"  ❌ Error procesando {formatted_date}: {e}")
        
        current_date += timedelta(days=1)
    
    return archivos_procesados > 0

def leer_datos_estacion(estacion_codigo, horas=24):
    """Lee los datos procesados de una estación para la ventana temporal seleccionada"""
    ahora = datetime.now(timezone.utc)
    inicio = ahora - timedelta(hours=horas)
    
    output_dir = f"{BASE_OUTPUT_DIR}/{ahora.year}/{estacion_codigo}/{ahora.month:02d}"
    
    if not os.path.exists(output_dir):
        return [], [], []
    
    timestamps = []
    amplitudes = []
    phases = []
    
    # Calcular cuántos días necesitamos leer basado en la ventana temporal
    dias_necesarios = (horas // 24) + 2  # +2 para asegurar cobertura
    
    # Leer archivos de los días necesarios
    for dias_antes in range(dias_necesarios):
        fecha_objetivo = (ahora - timedelta(days=dias_antes)).date()
        archivo_path = os.path.join(output_dir, f"{fecha_objetivo.strftime('%d-%m-%Y')}.txt")
        
        if os.path.exists(archivo_path) and os.path.getsize(archivo_path) > 100:
            try:
                with open(archivo_path, 'r') as file:
                    lineas_validas = 0
                    for line in file:
                        parts = line.strip().split()
                        if len(parts) >= 3:
                            try:
                                timestamp_str = parts[0]
                                if '.' in timestamp_str:
                                    timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d_%H:%M:%S.%f")
                                else:
                                    timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d_%H:%M:%S")
                                
                                timestamp = timestamp.replace(tzinfo=timezone.utc)
                                
                                # ⚠️ APLICAR CORRECCIÓN DE DESFASE DE 30 MINUTOS ⚠️
                                timestamp_corregido = timestamp + DESFASE_CORRECCION
                                
                                if timestamp_corregido >= inicio:
                                    amplitude = float(parts[1])
                                    phase = float(parts[2])
                                    
                                    timestamps.append(timestamp_corregido)  # Usar timestamp corregido
                                    amplitudes.append(amplitude)
                                    phases.append(phase)
                                    lineas_validas += 1
                                    
                            except ValueError:
                                continue
                    
                    if lineas_validas > 0:
                        print(f"    📖 {estacion_codigo}: {lineas_validas} líneas de {os.path.basename(archivo_path)}")
                        # Mostrar corrección aplicada
                        if lineas_validas == 1:  # Solo mostrar una vez por archivo
                            print(f"    ⚙️  Aplicada corrección de +30min a timestamps")
                    
            except Exception as e:
                print(f"    ❌ Error leyendo {archivo_path}: {e}")
    
    # Ordenar por timestamp
    if timestamps:
        sorted_data = sorted(zip(timestamps, amplitudes, phases))
        timestamps, amplitudes, phases = zip(*sorted_data)
    
    print(f"    📊 {estacion_codigo}: {len(timestamps)} puntos en {horas}h (con corrección +30min)")
    return list(timestamps), list(amplitudes), list(phases)

def calcular_amanecer_estacion(estacion_info, fecha):
    """Calcula los tiempos de amanecer para una estación"""
    tz = pytz.timezone(estacion_info['location'].timezone)
    
    try:
        sol_hoy = sun(estacion_info['location'].observer, date=fecha, tzinfo=tz)
        sunrise_utc_hoy = sol_hoy['sunrise'].astimezone(pytz.utc)
        return sunrise_utc_hoy
    except Exception as e:
        print(f"Error calculando amanecer para {estacion_info['nombre']}: {e}")
        return None

def crear_grafica_estacion(ax, estacion_codigo, estacion_info, timestamps, amplitudes, phases, horas_ventana):
    """Crea una gráfica individual para una estación con eventos solares"""
    
    if not timestamps or len(timestamps) < 5:
        ax.text(0.5, 0.5, f'Sin datos\n{estacion_codigo}', 
               horizontalalignment='center', verticalalignment='center',
               transform=ax.transAxes, fontsize=12, color='red')
        ax.set_title(f"{estacion_info['nombre']}\n({estacion_codigo})", 
                   fontsize=10, fontweight='bold')
        ax.set_facecolor('#f0f0f0')
        return
    
    # Convertir a arrays numpy
    ts = np.array(timestamps)
    amp = np.array(amplitudes)
    ph = np.array(phases)
    
    ahora_utc = datetime.now(timezone.utc)
    inicio_ventana = ahora_utc - timedelta(hours=horas_ventana)
    
    # Filtrar solo datos de la ventana temporal
    mascara = ts >= inicio_ventana
    ts_filtrado = ts[mascara]
    amp_filtrado = amp[mascara]
    ph_filtrado = ph[mascara]
    
    if len(ts_filtrado) == 0:
        ax.text(0.5, 0.5, f'Sin datos {horas_ventana}h\n{estacion_codigo}', 
               horizontalalignment='center', verticalalignment='center',
               transform=ax.transAxes, fontsize=10, color='red')
        ax.set_title(f"{estacion_info['nombre']}\n({estacion_codigo})", 
                   fontsize=10, fontweight='bold')
        return
    
    # Lista para elementos de leyenda
    legend_elements = []
    
    # Calcular y graficar amaneceres para todos los días en la ventana
    delta = timedelta(minutes=40)
    for dias in range((horas_ventana // 24) + 1):
        fecha = (ahora_utc - timedelta(days=dias)).date()
        sunrise_hoy = calcular_amanecer_estacion(estacion_info, fecha)
        
        if sunrise_hoy and (inicio_ventana <= sunrise_hoy <= ahora_utc):
            ax.axvspan(sunrise_hoy - delta, sunrise_hoy + delta,
                      color='green', alpha=0.3)
            # Añadir a leyenda solo una vez
            if not any('Amanecer' in elem.get_label() for elem in legend_elements):
                legend_elements.append(plt.Rectangle((0, 0), 1, 1, fc='green', alpha=0.3, label='Amanecer'))
    
    # Obtener y graficar eventos solares - MEJORADO
    eventos_solares = obtener_eventos_solares_ventana(horas_ventana)
    erupciones_intensas = obtener_erupciones_mas_intensas()
    
    colores_utilizados = set()
    
    for evento in eventos_solares:
        # Verificar si es una de las erupciones más intensas
        es_intensa = any(e['timestamp'] == evento['timestamp'] for e in erupciones_intensas)
        
        # Color según clasificación
        color_evento = {
            'C': 'yellow',
            'M': 'orange', 
            'X': 'red'
        }.get(evento['class'][0], 'gray')
        
        # Para eventos intensos: línea vertical gruesa
        if es_intensa:
            ax.axvline(x=evento['timestamp'], color=color_evento, linewidth=3, alpha=0.8)
            
            # Anotación especial para eventos intensos
            ax.annotate(f"🔥 {evento['class']}", 
                       xy=(evento['timestamp'], max(amp_filtrado) * 0.95),
                       xytext=(0, 10), textcoords='offset points',
                       ha='center', va='bottom', fontsize=9, fontweight='bold',
                       bbox=dict(boxstyle="round,pad=0.3", fc=color_evento, ec='black', lw=1, alpha=0.9))
        else:
            # Para eventos normales: banda sombreada
            inicio_evento = evento['timestamp'] - timedelta(minutes=30)
            fin_evento = evento['timestamp'] + timedelta(minutes=30)
            ax.axvspan(inicio_evento, fin_evento, color=color_evento, alpha=0.2)
            
            # Anotación normal
            ax.annotate(f"{evento['class']}", 
                       xy=(evento['timestamp'], max(amp_filtrado) * 0.85),
                       xytext=(0, 5), textcoords='offset points',
                       ha='center', va='bottom', fontsize=7,
                       bbox=dict(boxstyle="round,pad=0.2", fc=color_evento, alpha=0.7))
        
        # Añadir a leyenda solo una vez por color
        if color_evento not in colores_utilizados:
            clase_general = evento['class'][0]  # C, M o X
            if es_intensa:
                # Leyenda especial para eventos intensos
                legend_elements.append(plt.Line2D([0], [0], color=color_evento, lw=3, 
                                                label=f'🔥 {clase_general} Intensa'))
            else:
                legend_elements.append(plt.Rectangle((0, 0), 1, 1, fc=color_evento, alpha=0.3, 
                                                   label=f'{clase_general}'))
            colores_utilizados.add(color_evento)
    
    # Grilla
    ax.grid(True, alpha=0.3)
    
    # Graficar amplitud (SIN LABEL en leyenda)
    color_amp = estacion_info['color_amp']
    ax.plot(ts_filtrado, amp_filtrado, color=color_amp, linewidth=1.5)
    ax.set_ylabel('Amplitud', color=color_amp, fontsize=8)
    ax.tick_params(axis='y', labelcolor=color_amp, labelsize=8)
    
    # Graficar fase en eje secundario (SIN LABEL en leyenda)
    ax2 = ax.twinx()
    color_fase = estacion_info['color_fase']
    ax2.plot(ts_filtrado, ph_filtrado, color=color_fase, linewidth=1.5, alpha=0.8)
    ax2.set_ylabel('Fase', color=color_fase, fontsize=8)
    ax2.tick_params(axis='y', labelcolor=color_fase, labelsize=8)
    
    # Configurar eje X
    ax.set_xlim(inicio_ventana, ahora_utc)
    ax.set_xlabel('Hora (UT)', fontsize=8)
    ax.tick_params(axis='x', rotation=45, labelsize=7)
    
    # Título con contador de datos y eventos
    num_eventos = len(eventos_solares)
    num_intensas = len(erupciones_intensas)
    ax.set_title(f"{estacion_info['nombre']} ({estacion_codigo})\n{len(ts_filtrado)} datos, {num_intensas} intensas", 
               fontsize=8, fontweight='bold')
    
    # Leyenda solo con eventos solares y amanecer
    if legend_elements:
        ax.legend(handles=legend_elements, loc='upper left', fontsize=7)

def actualizar_todo():
    """Función que actualiza TODO al mismo tiempo: datos VLF y solares"""
    print(f"\n🔄 ACTUALIZACIÓN COMPLETA - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    # Actualizar datos solares primero
    obtener_fulguraciones_solares()
    
    # Mostrar erupciones más intensas
    erupciones_intensas = obtener_erupciones_mas_intensas()
    if erupciones_intensas:
        print(f"\n🔥 ERUPCIONES MÁS INTENSAS (24h):")
        for evento in erupciones_intensas:
            print(f"   ⚡ {evento['timestamp'].strftime('%H:%M UT')} - Clase {evento['class']}")
    
    # Luego actualizar datos VLF de todas las estaciones
    for estacion in ESTACIONES.keys():
        try:
            print(f"\n--- {estacion} ---")
            if descargar_datos_estacion(estacion):
                time.sleep(1)  # Pausa más corta
                if procesar_con_vtsidex(estacion):
                    print(f"✅ {estacion}: Procesamiento completado")
                else:
                    print(f"⚠ {estacion}: Problemas en el procesamiento")
            else:
                print(f"❌ {estacion}: No se pudieron descargar datos")
                
        except Exception as e:
            print(f"❌ Error actualizando {estacion}: {e}")
    
    print(f"\n✅ ACTUALIZACIÓN COMPLETA TERMINADA - {datetime.now().strftime('%H:%M:%S')}")

def actualizar_panel(frame):
    """Función de actualización para el panel - SOLO LECTURA DE DATOS"""
    try:
        plt.clf()
        
        # Crear layout de 2x3 para las 6 estaciones
        gs = gridspec.GridSpec(2, 3, hspace=0.5, wspace=0.4)
        
        print(f"\n📊 Leyendo gráficas - {datetime.now().strftime('%H:%M:%S')} - Ventana: {VENTANA_TIEMPO}h")
        print(f"⚙️  Aplicando corrección de +30min a todos los timestamps")
        
        # Obtener y mostrar erupciones intensas
        erupciones_intensas = obtener_erupciones_mas_intensas()
        if erupciones_intensas:
            print(f"🔥 Erupciones intensas detectadas:")
            for evento in erupciones_intensas:
                print(f"   ⚡ {evento['timestamp'].strftime('%H:%M UT')} - Clase {evento['class']}")
        
        # Leer y graficar cada estación
        for idx, (estacion_codigo, estacion_info) in enumerate(ESTACIONES.items()):
            fila = idx // 3
            columna = idx % 3
            
            ax = plt.subplot(gs[fila, columna])
            
            # Leer datos de la estación para la ventana temporal actual
            timestamps, amplitudes, phases = leer_datos_estacion(estacion_codigo, VENTANA_TIEMPO)
            
            # Crear gráfica con eventos solares
            crear_grafica_estacion(ax, estacion_codigo, estacion_info, timestamps, amplitudes, phases, VENTANA_TIEMPO)
        
        # Título principal con info solar y ventana temporal
        tiempo_actual = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UT")
        eventos_solares = obtener_eventos_solares_ventana(VENTANA_TIEMPO)
        num_eventos = len(eventos_solares)
        num_intensas = len(erupciones_intensas)
        
        # Calcular próxima actualización
        proxima_actualizacion = datetime.now() + timedelta(seconds=INTERVALO_ACTUALIZACION_COMPLETA)
        
        plt.suptitle(f'ESTACIONES VLF y Eventos solares | Últimas {VENTANA_TIEMPO}h | {num_eventos} eventos ({num_intensas} intensos) | Actualizado: {tiempo_actual} |'
                     , fontsize=12, fontweight='bold', y=0.95)
        
        plt.tight_layout() 
        plt.subplots_adjust(top=0.90)
        
    except Exception as e:
        print(f"❌ Error en actualizar_panel: {e}")
        plt.clf()
        plt.text(0.5, 0.5, f'Error: {str(e)}', 
                horizontalalignment='center', verticalalignment='center',
                transform=plt.gca().transAxes, fontsize=10, color='red')

def main():
    """Función principal"""
    print("🚀 PANEL DE MONITOREO VLF + FULGURACIONES SOLARES")
    print("="*60)
    print("Estaciones:", list(ESTACIONES.keys()))
    
    # Seleccionar ventana temporal al inicio
    seleccionar_ventana_temporal()
    
    print(f"\n⚙️ CONFIGURACIÓN DE ACTUALIZACIÓN:")
    print(f"  📊 Actualización completa: cada 5 minutos")
    print(f"  📥 Incluye: Descarga VLF + Procesamiento + Datos solares")
    print(f"  ⏰ Ventana temporal: {VENTANA_TIEMPO} horas")
    print(f"  ⚙️  Corrección de tiempo: +30min aplicada")
    print(f"  🔥 Erupciones intensas: línea vertical + emoji fuego")
    print(f"  🚀 Iniciando primera actualización completa...")
    print("Presiona Ctrl+C para detener")
    print("="*60)
    
    # Verificar conexión SSH
    print("🔍 Verificando conexión SSH...")
    test_cmd = "ssh -o BatchMode=yes -o ConnectTimeout=5 radzac@192.168.1.67 'echo ✅ SSH OK'"
    result = subprocess.run(test_cmd, shell=True, capture_output=True, text=True)
    if "OK" in result.stdout:
        print("✅ Conexión SSH configurada correctamente")
    else:
        print("❌ Problema con SSH. Ejecuta:")
        print("   ssh-keygen -t rsa")
        print("   ssh-copy-id radzac@192.168.1.67")
        return
    
    # Realizar primera actualización completa
    actualizar_todo()
    
    # Crear figura
    fig = plt.figure(figsize=(15, 11))
    
    # Contador para actualización completa
    ultima_actualizacion_completa = time.time()
    
    def animar(frame):
        nonlocal ultima_actualizacion_completa
        
        ahora = time.time()
        
        # Actualizar TODO cada 5 minutos
        if ahora - ultima_actualizacion_completa > INTERVALO_ACTUALIZACION_COMPLETA:
            print(f"\n🔄 INICIANDO ACTUALIZACIÓN COMPLETA - {datetime.now().strftime('%H:%M:%S')}")
            threading.Thread(target=actualizar_todo, daemon=True).start()
            ultima_actualizacion_completa = ahora
        
        # Siempre actualizar el panel (solo lectura de datos)
        actualizar_panel(frame)
    
    try:
        # Crear animación que se actualiza cada 30 segundos (solo para lectura)
        anim = FuncAnimation(fig, animar, interval=60000, cache_frame_data=False)
        
        # Mostrar el panel
        plt.show()
        
    except KeyboardInterrupt:
        print("\n⏹️ Panel detenido por el usuario")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()