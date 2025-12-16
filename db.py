import mysql.connector
from mysql.connector import pooling

MYSQL_PASSWORD = "******" 

pool = pooling.MySQLConnectionPool(
    pool_name="app_pool",
    pool_size=5,
    host="localhost",
    user="root",
    password=MYSQL_PASSWORD,
    database="universite",
    autocommit=False
)

def get_conn():
    try:
        conn = pool.get_connection()
        return conn
    except mysql.connector.Error as err:
        print(f"Erreur de connexion au pool: {err}")
        return None

if __name__ == '__main__':
    conn = get_conn()
    if conn and conn.is_connected():
        print("db.py : Connexion au pool réussie.")
        conn.close() 
    else:

        print("db.py : Échec de la connexion.")
