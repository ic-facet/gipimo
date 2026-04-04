import random
import time

from db_dataraygpt import register_data_ray_gpt
from datetime import datetime

while True:
    # Get the current date and time
    seconds_1 = time.time()
    now = datetime.now()
    datetime_utc = now.strftime("%Y-%m-%d %H:%M:%S")
    #.strftime("%Y-%m-%d %H:%M:%S")
    intensidad = random.randint(0, 10)
    campo_kVm = random.randint(0, 10) + (round(random.random(),2))
    temp_C = random.randint(0, 10) + (round(random.random(),2))
    humedad_rh = random.randint(0, 10) + (round(random.random(),2))
    presion_hPa  = random.randint(0, 10) + (round(random.random(),2))
    cpm_escalado  = random.randint(0, 10) + (round(random.random(),2))
    avg_cpm_reciente  = random.randint(0, 10) + (round(random.random(),2))

    register_data_ray_gpt(datetime_utc, intensidad,campo_kVm,temp_C,humedad_rh,presion_hPa,cpm_escalado,avg_cpm_reciente)
    
    seconds_2 = time.time()
    diferencia = 2- (seconds_2 - seconds_1) - 0.0088
    
    if diferencia<0:
        diferencia=diferencia*-1

    print(f"{datetime_utc},{intensidad},{campo_kVm},{temp_C},{humedad_rh},{presion_hPa},{cpm_escalado},{avg_cpm_reciente} ")
 
    time.sleep(diferencia)
