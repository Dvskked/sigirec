import mysql.connector
from mysql.connector import Error

def obtener_conexion():
    try:
        conexion = mysql.connector.connect(
            host="b8y5mp8b50lm12bqe1og-mysql.services.clever-cloud.com",
            user="umjhpxyzaojbzblh", # El usuario que te muestra Clever Cloud en la pestaña Information
            password="0O3mCa7Ykc3BcQow97Y4", # La contraseña que te muestra Clever Cloud en la pestaña Information
            database="b8y5mp8b50lm12bqe1og",
            port=3306
        )
        return conexion
    except Error as e:
        print(f"Error al conectar con MySQL: {e}")
        return None
