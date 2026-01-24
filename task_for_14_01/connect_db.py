import psycopg


conn = psycopg.connect(
    dbname="postgres",
    user= 'postgres',
    password = 'postgres',
    host = 'localhost',
    port = '5433',
)
#для использование скюл запытов
cursor = conn.cursor()
cursor.execute('SELECT version();')
db_version = cursor.fetchone()
print(db_version)
cursor.close()
conn.close()
