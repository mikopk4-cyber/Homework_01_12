import psycopg

host = 'localhost'
port = '5433'
user = 'postgres'
password = 'postgres'





with psycopg.connect(f'host={host} port={port} user={user} password={password} dbname=online_cinema2') as conn:
    with conn.cursor() as cursor:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS movies(
            id SERIAL PRIMARY KEY,
            title VARCHAR(100) NOT NULL,
            author VARCHAR(100) NOT NULL,
            year VARCHAR(10) NOT NULL,
            ganre VARCHAR(10) NOT NULL
        );
        """)




