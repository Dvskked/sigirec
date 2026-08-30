import mysql.connector
from mysql.connector import Error

def obtener_conexion():
    try:
        conexion = mysql.connector.connect(  #Las credenciales de la base de datos las tengo solamente yo, entonces no es posible hace la conexion con sigirec Origins
            host="####################",
            user="###########################", 
            password="################", 
            database="##################",
            port=######
        )


        #
        return conexion
    except Error as e:
        print(f"Error al conectar con MySQL: {e}")
        return None
