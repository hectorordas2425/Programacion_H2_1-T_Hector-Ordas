import mysql.connector

def conectar_db():
    try:
        conexion= mysql.connector.connect(
        host="localhost",
        user="root",
        password="curso",
        database="app_tienda"
        )
        if conexion.is_connected():
            print("Conexión a MySQL establecida.")
            return conexion
    except ValueError:
        print("Error al conectar a MySQL")