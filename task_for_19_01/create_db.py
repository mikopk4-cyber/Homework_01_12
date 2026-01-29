

import psycopg

host = 'localhost'
port = '5433'
user = 'postgres'
password = 'postgres'


def create_db():
    try:
        with psycopg.connect(f'host={host} port={port} user={user} password={password} dbname=postgres', autocommit=True) as conn:
            with conn.cursor() as cursor:
                cursor.execute('CREATE DATABASE library WITH ENCODING=UTF8')
                print('Database created')
    except psycopg.OperationalError:
        print('Database already exists')


def create_table():
    try:
        with psycopg.connect(f'host={host} port={port} user={user} password={password} dbname=library') as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS book(
                id SERIAL PRIMARY KEY,
                title VARCHAR(255) NOT NULL
                );
                """)

                cursor.execute("""
                CREATE TABLE IF NOT EXISTS book_copy(
                id SERIAL PRIMARY KEY,
                book_id INTEGER NOT NULL,
                description VARCHAR(255) NOT NULL,
                CONSTRAINT book_fk 
                FOREIGN KEY (book_id) 
                REFERENCES book(id)
                ON DELETE CASCADE
                );
                """)
                
    except psycopg.OperationalError:
        print('Table already exists')

if __name__ == '__main__':
    create_db()
    create_table()