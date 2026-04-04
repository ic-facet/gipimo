import mysql.connector
import json
import db_config
import requests
import schedule
import time
from datetime import date,datetime
#DB_CONFIG = db_config.DB_CONFIG

url_rgpt = "http://idawis-uaz.ddns.net:3000/insertRayGPT"
url_radob = "http://idawis-uaz.ddns.net:3000/insertRadob"

frec_rgpt = 300
frec_radob = 360

# Establish a connection to the MySQL database
mydb = mysql.connector.connect(**db_config.DB_CONFIG)
cursor = mydb.cursor()
cursor = mydb.cursor(dictionary=True)

now = datetime.now()
last_op = now.strftime("%Y-%m-%d %H:%M:%S")
print("Starting: ",last_op)


def sendRayGPT():
    sql_query = "SELECT datetime_utc, \
             FORMAT(intensidad, 2) AS intensidad,\
             FORMAT(campo_kVm, 2) AS campo_kVm,\
             FORMAT(temp_C, 2) AS temp_C,\
             FORMAT(humedad_rh, 2) AS humedad_rh,\
             FORMAT(presion_hPa, 2) AS presion_hPa,\
             FORMAT(campo_kVm, 2) AS campo_kVm,\
             FORMAT(cpm_escalado, 2) AS cpm_escalado,\
             FORMAT(campo_kVm, 2) AS campo_kVm,\
             FORMAT(avg_cpm_reciente, 2) AS avg_cpm_reciente \
             FROM data_ray_gpt where sended='N' LIMIT 300;"
    cursor.execute(sql_query)
    data = cursor.fetchall()
    #json_data = json.dumps(data)
    json_data = json.dumps(data, indent=4) 
    data = json.loads(json_data)
    total_registros=0
    try:
        response = requests.post(url_rgpt, json=data)
    except requests.exceptions.HTTPError as e:
        # Handle HTTP errors (e.g., 404 Not Found, 500 Internal Server Error)
        response = "HTTP Error occurred: "+str(e)
    except requests.exceptions.ConnectionError as e:
        # Handle network-related errors (e.g., no internet connection, DNS failure)
        response = "Connection Error occurred: "+str(e)
    except requests.exceptions.Timeout as e:
        # Handle request timeouts
        response = "Timeout Error occurred: "+str(e)
    except requests.exceptions.RequestException as e:
        # Handle any other general requests-related exceptions
        response = "An unexpected Requests error occurred: "+str(e)
    finally:
        # This block will always execute, regardless of whether an exception occurred
        resdata = response.json()
        for rd in resdata:
            date_temp = rd['datetime_utc']
            date = date_temp[:10]
            time = date_temp[11:]
            datetime_temp=date+" "+time[:8]
            sql="UPDATE data_ray_gpt set sended = 'Y' WHERE DATE_FORMAT(datetime_utc, '%Y-%m-%d %H:%i:%s') = '"+datetime_temp+"'"
            total_registros=total_registros+1
            cursor.execute(sql)
            mydb.commit()
        sql="delete from data_ray_gpt where sended='Y'"
        cursor.execute(sql)
        mydb.commit()
        now = datetime.now()
        last_op = now.strftime("%Y-%m-%d %H:%M:%S")
        print(f"RayGPT update: {response} {total_registros} ",last_op)

def sendRadob():
    sql_query = "SELECT datetime_utc, FORMAT(ua, 10) AS ua FROM data_radob where sended='N' LIMIT 300;"
    cursor.execute(sql_query)
    data = cursor.fetchall()
    #json_data = json.dumps(data)
    json_data = json.dumps(data, indent=4) 
    data = json.loads(json_data)
    total_registros = 0
    try:
        response = requests.post(url_radob, json=data)
    except requests.exceptions.HTTPError as e:
        # Handle HTTP errors (e.g., 404 Not Found, 500 Internal Server Error)
        response = "HTTP Error occurred: "+str(e)
    except requests.exceptions.ConnectionError as e:
        # Handle network-related errors (e.g., no internet connection, DNS failure)
        response = "Connection Error occurred: "+str(e)
    except requests.exceptions.Timeout as e:
        # Handle request timeouts
        response = "Timeout Error occurred: "+str(e)
    except requests.exceptions.RequestException as e:
        # Handle any other general requests-related exceptions
        response = "An unexpected Requests error occurred: "+str(e)
    finally:
        # This block will always execute, regardless of whether an exception occurred
        resdata = response.json()
        for rd in resdata:
            date_temp = rd['datetime_utc']
            date = date_temp[:10]
            time = date_temp[11:]
            datetime_temp=date+" "+time[:8]
            sql="UPDATE data_radob set sended = 'Y' WHERE DATE_FORMAT(datetime_utc, '%Y-%m-%d %H:%i:%s') = '"+datetime_temp+"'"
            total_registros=total_registros+1
            cursor.execute(sql)
            mydb.commit()
        sql="delete from data_radob where sended='Y'"
        cursor.execute(sql)
        mydb.commit()
        now = datetime.now()
        last_op = now.strftime("%Y-%m-%d %H:%M:%S")
        print(f"Radob update: {response} {total_registros} ",last_op)

schedule.every(frec_rgpt).seconds.do(sendRayGPT)
schedule.every(frec_radob).seconds.do(sendRadob)

while True:
    schedule.run_pending()
    time.sleep(1)
    