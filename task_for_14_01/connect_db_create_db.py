
import psycopg

host = 'localhost'
port = '5433'
user = 'postgres'
password = 'postgres'


#with open psycopg.connect(host=host, port=port, user=user, password=password, database='postgres') as conn:

with psycopg.connect(f'host={host} port={port} user={user} password={password} dbname=postgres') as conn:
    conn.autocommit = True
    with conn.cursor() as cursor:
        cursor.execute("CREATE DATABASE online_cinema2 WITH ENCODING 'utf8';")
        print("Successfully created database 'online_cinema2'")
