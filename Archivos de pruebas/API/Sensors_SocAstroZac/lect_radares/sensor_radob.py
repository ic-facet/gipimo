import random
import time

from db_dataraygpt import register_data_radob
from datetime import datetime

while True:
    # Get the current date and time
    seconds_1 = time.time()
    now = datetime.now()
    datetime_utc = now.strftime("%Y-%m-%d %H:%M:%S")
    ua = random.randint(0, 10) + (round(random.random(),2))

    register_data_radob(datetime_utc, ua)
    seconds_2 = time.time()
    diferencia = 5 - (seconds_2 - seconds_1) - 0.0088
    if diferencia<0:
        diferencia=diferencia*-1

    print(f"{datetime_utc},{ua}")
    
    time.sleep(diferencia)
