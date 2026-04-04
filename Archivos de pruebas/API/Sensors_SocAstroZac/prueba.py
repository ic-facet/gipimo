import mysql.connector

try:
    # Establish a connection
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="adquisiciones"
    )

    # Create a cursor object
    mycursor = mydb.cursor()

    # Execute a query
    mycursor.execute("SELECT * FROM acciones")

    # Fetch results
    myresult = mycursor.fetchall()

    for x in myresult:
        print(x)

except mysql.connector.Error as err:
    print(f"Error: {err}")

finally:
    # Close the connection
    if 'mydb' in locals() and mydb.is_connected():
        mycursor.close()
        mydb.close()
        print("MySQL connection closed.")