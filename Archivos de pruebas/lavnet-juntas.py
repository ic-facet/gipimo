import os
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta, timezone
import locale
from astral import LocationInfo
from astral.sun import sun
import pytz

# Establecer locale a español
locale.setlocale(locale.LC_TIME, 'es_ES.utf8')  # O 'es_MX.utf8'

# Directorios
dir_path = "/home/ivan/Documentos/LAVNet-ZAC/2025/NAA/09"
output_dir = "/home/ivan/Documentos/LAVNet-ZAC/imagenes/2025/NAA/09"
os.makedirs(output_dir, exist_ok=True)

# Ubicación
ciudad = LocationInfo("NAA", "Estados Unidos", "America/Halifax", 44.6333, -67.2667)  # Cutler, Maine

# Leer archivos
def read_files_in_directory(directory):
    data = []
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r') as file:
                lines = file.readlines()
                timestamps = []
                amplitudes = []
                phases = []
                
                for line in lines:
                    parts = line.strip().split()
                    if len(parts) == 3:
                        timestamp = datetime.strptime(parts[0], "%Y-%m-%d_%H:%M:%S.%f")
                        timestamp = timestamp.replace(tzinfo=timezone.utc)
                        amplitude = float(parts[1])
                        phase = float(parts[2])
                        
                        timestamps.append(timestamp)
                        amplitudes.append(amplitude)
                        phases.append(phase)
                
                if timestamps:
                    data.append({
                        "timestamps": np.array(timestamps),
                        "amplitudes": np.array(amplitudes),
                        "phases": np.array(phases),
                    })
    return data

# Leer
data = read_files_in_directory(dir_path)

# Procesar
for dataset in data:
    timestamps = dataset["timestamps"]
    amplitudes = dataset["amplitudes"]
    phases = dataset["phases"]
    
    if len(timestamps) > 0:
        fecha = timestamps[0]
        mes_nombre = fecha.strftime('%B').capitalize()
        anio = fecha.year
        dia = fecha.date()
        tz = pytz.timezone(ciudad.timezone)

        # Día actual y anterior
        sol_hoy = sun(ciudad.observer, date=dia, tzinfo=tz)
        sol_ayer = sun(ciudad.observer, date=dia - timedelta(days=1), tzinfo=tz)

        # Convertir a UTC
        sunrise_utc = sol_hoy['sunrise'].astimezone(pytz.utc)

        # Margen de ±35 minutos para sombrear
        delta = timedelta(minutes=35)

        # Crear figura con un solo panel combinado
        fig, ax1 = plt.subplots(figsize=(12, 6))

        # Banda de amanecer
        ax1.axvspan(sunrise_utc - delta, sunrise_utc + delta,
                    color='green', alpha=0.3, label='Amanecer')

        # ---- Selección manual de evento y anotación ----
        hora_inicio = datetime(fecha.year, fecha.month, fecha.day, 18, 5, 0, tzinfo=timezone.utc)
        hora_fin = datetime(fecha.year, fecha.month, fecha.day, 19, 40, 0, tzinfo=timezone.utc)
        etiqueta = "Clase M5.2"

        # Sombra para el evento
        ax1.axvspan(hora_inicio, hora_fin, color='orange', alpha=0.3, label=etiqueta)

        # Anotación en el gráfico
        hora_media = hora_inicio + (hora_fin - hora_inicio) / 2
        ax1.annotate(etiqueta, xy=(hora_media, max(amplitudes)),
                     xytext=(0,2), textcoords='offset points',
                     ha='center', va='bottom', fontsize=10,
                     bbox=dict(boxstyle="round,pad=0.3", fc="orange", ec="black", lw=1))

        # Grilla
        ax1.grid(True)

        # Amplitud
        ax1.plot(timestamps, amplitudes, label="Amplitud", color='blue')
        ax1.set_ylabel('Amplitud', color='blue')
        ax1.tick_params(axis='y', labelcolor='blue')

        # Fase
        ax2 = ax1.twinx()
        ax2.plot(timestamps, phases, label="Fase", color='red')
        ax2.set_ylabel('Fase', color='red')
        ax2.tick_params(axis='y', labelcolor='red')

        # Leyenda combinada
        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

        # Eje X
        ax1.set_xlabel('Fecha y Hora (UT)')
        plt.xticks(rotation=0)

        # Título
        plt.title(f"{mes_nombre} {anio} NAA", fontsize=14)
        plt.tight_layout()

        # Guardar
        file_name = f"{mes_nombre}_{anio}_{fecha.strftime('%d-%H-%M-%S')}.png"
        file_path = os.path.join(output_dir, file_name)
        plt.savefig(file_path, dpi=250)
        plt.show()
        print(f"Gráfica guardada en {file_path}")
    else:
        print("No hay datos para graficar en este archivo.")
