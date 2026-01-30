import psycopg
from psycopg import errors

host = 'localhost'
port = '5433'
user = 'postgres'
password = 'postgres'
db_name = 'client_service_new_3'

def create():
    try:
        with psycopg.connect(f'host={host} port={port} user={user} password={password} dbname=postgres', autocommit=True) as conn:
            with conn.cursor() as cur:
                cur.execute(f'CREATE DATABASE {db_name} WITH ENCODING=UTF8')
                print(f'Database {db_name} created')
    except errors.DuplicateDatabase:
        print(f'Database {db_name} already exists')
    except Exception as e:
        print(f'Error: {e}')

def create_table():
    try:
        with psycopg.connect(f'host={host} port={port} user={user} password={password} dbname={db_name}') as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS clients (
                        id SERIAL PRIMARY KEY,
                        surname VARCHAR(255) NOT NULL,
                        name VARCHAR(255) NOT NULL,
                        patronymic VARCHAR(255) NOT NULL,
                        email VARCHAR(255) NOT NULL,
                        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                    );
                """)

                cur.execute("""
                    CREATE TABLE IF NOT EXISTS address (
                        id SERIAL PRIMARY KEY,
                        country VARCHAR(255) NOT NULL,
                        region VARCHAR(255) NOT NULL,
                        area VARCHAR(255) NOT NULL,
                        city VARCHAR(255) NOT NULL,
                        street VARCHAR(255) NOT NULL,
                        building INTEGER NOT NULL,
                        apartment INTEGER NOT NULL,
                        entrance VARCHAR(255) NOT NULL,
                        room INTEGER NOT NULL,
                        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                        clients_id INTEGER NOT NULL UNIQUE,
                        CONSTRAINT clients_address_fk FOREIGN KEY (clients_id) REFERENCES clients(id) ON DELETE CASCADE
                    );
                """)

                cur.execute("""
                    CREATE TABLE IF NOT EXISTS phone (
                        id SERIAL PRIMARY KEY,
                        phone VARCHAR(20) NOT NULL,
                        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                        clients_id INTEGER NOT NULL,
                        CONSTRAINT clients_phone_fk FOREIGN KEY (clients_id) REFERENCES clients(id) ON DELETE CASCADE
                    );
                """)

                cur.execute("""
                    CREATE TABLE IF NOT EXISTS currency (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(255) NOT NULL,
                        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                    );
                """)

                cur.execute("""
                    CREATE TABLE IF NOT EXISTS account (
                        id SERIAL PRIMARY KEY,
                        amount NUMERIC(18,2) NOT NULL,
                        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                        currency_id INTEGER NOT NULL,
                        CONSTRAINT currency_account_fk FOREIGN KEY (currency_id) REFERENCES currency(id)
                    );
                """)

                cur.execute("""
                    CREATE TABLE IF NOT EXISTS client_account(
                        clients_id INTEGER NOT NULL,
                        account_id INTEGER NOT NULL,
                        PRIMARY KEY(clients_id, account_id),
                        CONSTRAINT clients_account_fk FOREIGN KEY(clients_id) REFERENCES clients(id) ON DELETE CASCADE,
                        CONSTRAINT client_account_account_fk FOREIGN KEY(account_id) REFERENCES account(id) ON DELETE CASCADE
                    );
                """)

                cur.execute("""
                    CREATE TABLE IF NOT EXISTS role (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(255) NOT NULL,
                        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                    );
                """)

                cur.execute("""
                    CREATE TABLE IF NOT EXISTS status (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(255) NOT NULL,
                        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                    );
                """)

                cur.execute("""
                    CREATE TABLE IF NOT EXISTS "user" (
                        id SERIAL PRIMARY KEY,
                        login VARCHAR(255) NOT NULL,
                        password_hash VARCHAR(255) NOT NULL,
                        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                        role_id INTEGER NOT NULL,
                        status_id INTEGER NOT NULL,
                        CONSTRAINT user_role_fk FOREIGN KEY(role_id) REFERENCES role(id) ON DELETE CASCADE,
                        CONSTRAINT user_status_fk FOREIGN KEY(status_id) REFERENCES status(id) ON DELETE CASCADE
                    );
                """)

                conn.commit()
                print('TABLES created')

    except Exception as e:
        print(f'Error: {e}')

if __name__ == '__main__':
    create()
    create_table()
