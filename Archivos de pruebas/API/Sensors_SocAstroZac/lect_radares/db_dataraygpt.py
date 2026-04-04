import mysql.connector

import db_config

# Database connection details

def register_data_ray_gpt(datetime_utc,intensidad,campo_kVm,temp_C,humedad_rh,presion_hPa,cpm_escalado,avg_cpm_reciente):
    """
    Registers data from ray sensor
    """
    try:
        # Establish a connection to the MySQL database
        mydb = mysql.connector.connect(**db_config.DB_CONFIG)
        cursor = mydb.cursor()
        sended = 'N'
        # SQL INSERT statement
        sql = "INSERT INTO data_ray_gpt (datetime_utc,intensidad,campo_kVm,temp_C,humedad_rh,presion_hPa,cpm_escalado,avg_cpm_reciente,sended) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        values = (datetime_utc,intensidad,campo_kVm,temp_C,humedad_rh,presion_hPa,cpm_escalado,avg_cpm_reciente,sended)

        # Execute the SQL query
        cursor.execute(sql, values)

        # Commit the changes to the database
        mydb.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'mydb' in locals() and mydb.is_connected():
            mydb.close()

def register_data_radob(datetime_utc,ua):
    """
    Registers data from radob sensor
    """
    try:
        # Establish a connection to the MySQL database
        mydb = mysql.connector.connect(**db_config.DB_CONFIG)
        cursor = mydb.cursor()
        sended = 'N'
        # SQL INSERT statement
        sql = "INSERT INTO data_radob (datetime_utc,ua,sended) VALUES (%s,%s,%s)"
        values = (datetime_utc,ua,sended)

        # Execute the SQL query
        cursor.execute(sql, values)

        # Commit the changes to the database
        mydb.commit()

        #print(f"{cursor.rowcount} record inserted successfully.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        # Close the cursor and connection
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'mydb' in locals() and mydb.is_connected():
            mydb.close()

