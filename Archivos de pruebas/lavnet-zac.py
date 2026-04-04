import os
from datetime import datetime, timedelta

# Ruta base para el directorio de datos
data_dir = "/home/ivan/vlfrx-tools-0.9p/Datos_Sid"

# Solicitar al usuario el año, el mes y la estación
year = int(input("Ingresa el año (por ejemplo, 2025): "))
month = int(input("Ingresa el mes (1-12): "))
station = input("Ingresa la estación (por ejemplo, NAA): ")

# Ruta de destino para guardar los archivos generados
output_dir = f"/home/ivan/Documentos/LAVNet-ZAC/{year}/{station}/{month:02d}"
os.makedirs(output_dir, exist_ok=True)  # Crear el directorio si no existe

# Configurar el mes completo
start_date = datetime(year, month, 1)  # Primer día del mes
end_date = (start_date + timedelta(days=32)).replace(day=1) - timedelta(days=1)  

# Iterar sobre las fechas en el rango
current_date = start_date
while current_date <= end_date:
    # Formatear la fecha para el comando
    formatted_date = current_date.strftime("%Y-%m-%d")
    
    # Generar el rango horario
    start_time = f"{formatted_date}_00"
    end_time = f"{formatted_date}_24"
    
    # Generar nombre del archivo de salida
    output_filename = current_date.strftime("%d-%m-%Y.txt")
    output_path = os.path.join(output_dir, output_filename)
    
    # Comando `vtsidex` con los parámetros correctos
    command = f"vtsidex -m {station} -a10 -h360 -T{start_time},{end_time} {data_dir} > {output_path}"
    print(f"Ejecutando: {command}")
    
    # Ejecutar el comando
    os.system(command)
    
    # Avanzar al siguiente día
    current_date += timedelta(days=1)

print(f"Proceso completado. Archivos generados en: {output_dir}")
