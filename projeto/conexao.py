import psycopg2

def conectar():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="academia",
            user="postgres",
            password="1324"
        )
        return conn
    except Exception as e:
        print("Erro ao conectar no banco:", e)
        return None
