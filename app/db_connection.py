import os
import psycopg
from dotenv import load_dotenv

# Cargar las variables del archivo .env
load_dotenv()

def obtener_conexion():
    # Obtener la URL de la base de datos desde la variable de entorno
    database_url = os.getenv('DATABASE_URL')

    if not database_url:
        raise ValueError("La variable de entorno DATABASE_URL no está definida.")
    
    # Establecer la conexión con la base de datos usando la URL
    conn = psycopg.connect(database_url)
    return conn
