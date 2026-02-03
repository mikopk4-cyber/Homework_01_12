import psycopg


host = 'localhost'
port = '5433'
user = 'postgres'
password = 'postgres'
db_name = 'courses_students'


def create_db():
    try:
        with psycopg.connect(f'host {host} port {port} user{user} password{password} dbname=postgres', autocommit=True) as conn:
            with conn.cursor() as cur:
                cur.execute(f"CREATE DATABASE {db_name} WITH ENCODING 'UTF8'")
                print('Database created')
    except psycopg.OperationalError:
        print('Database already exists')
    except Exception as e:
        print(e)


def create_tables():
    try:
        with psycopg.connect(f'host {host} port {port} user{user} password{password} dbname={db_name}', autocommit=True) as conn:
            with conn.cursor() as cur:
                cur.execute("""CREATE TABLE IF NOT EXISTS students(
                            id SERIAL PRIMARY KEY,
                            first_name VARCHAR(255),
                            last_name VARCHAR(255),
                            email VARCHAR(255),
                            average_note INTEGER NOT NULL
                            );
                            """)

                cur.execute("""CREATE TABLE IF NOT EXISTS courses(
                            id SERIAL PRIMARY KEY,
                            course_id INTEGER NOT NULL,
                            course_name VARCHAR(255),
                            course_quantity_week INTEGER NOT NULL
                            );
                            """)

                cur.execute("""CREATE TABLE IF NOT EXISTS students_courses(
                            students_id INTEGER NOT NULL,
                            course_id INTEGER NOT NULL,
                            PRIMARY KEY(students_id, course_id),
                            
                            CONSTRAINT fk_students_courses 
                            FOREIGN KEY (students_id)
                            REFERENCES students(id)
                            ON DELETE CASCADE
                            
                            CONSTRAINT fk_courses 
                            FOREIGN KEY (course_id)
                            REFERENCES courses(id)
                            ON DELETE CASCADE
                            );
                            """)

                cur.execute("""
                INSERT INTO students (first_name, last_name, email, average_note)
                 VALUES 
                 ('Marina', 'Marinko', 'marina.karina@gmail.com', 89),
                 ('Mischa', 'Maruso', 'mischa.maruso@gmail.com', 87),
                 ('Kiril', 'Titarenko', 'kiril@gmail.com', 78),
                 ('Illa', 'Stechenko', 'illa34@gmail.com', 56),
                 ('Kolya', 'Zertii', 'kolya22@gmail.com', 99)
                 """)

                cur.execute("""
                INSERT INTO courses (course_id, course_name, course_quantity_week)
                VALUES
                (123, 'Math', 4),
                (231, 'Machine Learning', 5),
                (345, 'Sport', 3),
                (789, 'Philosophy', 2),
                (987, 'History', 1)
    
                """)
                cur.execute("""
                INSERT INTO students_courses (students_id, course_id)
                VALUES
                (1,1), -- Marina at Math and History
                (1,2), -- Kiril at Sport
                (2,1), -- Kolya at Philosophy and Sport
                (2,2), -- Illa at History
                (3,1), -- Mischa at Philosophy and Machine Learning
                (3,2), -- Kolya at Math and History
                (3,3), -- Marina at Sport and Machine Learning
                """)

    except psycopg.OperationalError:
        print('Table already exists')
    except Exception as e:
        print(e)

def get_students():
    try:
        with psycopg.connect(f'host {host} port {port} user{user} password{password} dbname={db_name}', autocommit=True) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                SELECT 
                s.id,
                s.first_name,
                s.last_name,
                s.email,
                s.average_note,
                COUNT (c.id) AS courses_count,
                ARRAY_AGG(c.courses_name ORDER BY c.course_name)
                     FILTER (WHERE c.course_name IS NOT NULL) AS courses
                FROM students s
                LEFT JOIN students_courses sc ON s.id = sc.student_id
                LEFT JOIN courses c ON sc.course_id = c.id
                GROUP BY s.id, s.first_name, s.last_name, s.email, s.average_note
                ORDER BY s.last_name
                ;
                """)

                cur.execute("""
                SELECT 
                    c.id,
                    c.course_name,
                    COUNT(s.id) AS students_count,
                    ARRAY_AGG(
                         s.last_name || ' ' || s.first_name
                         ORDER BY s.last_name
                    )
                    FILTER (WHERE s.id IS NOT NULL) AS students
                FROM courses c
                LEFT JOIN students_courses sc ON  c.id = sc.course_id
                LEFT JOIN students s ON sc.student_id = s.id
                GROUP BY c.id, c.course_name
                ORDER BY c.course_name; """)

    except psycopg.OperationalError:
        print('Table already exists')

    except Exception as e:
        print(e)




