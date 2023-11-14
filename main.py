import psycopg2


def create_db(conn):
    cur.execute('''
    CREATE TABLE IF NOT EXISTS clients(
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(30) NOT NULL,
    last_name VARCHAR(30) NOT NULL);
     ''')
    conn.commit()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS client_info(
    id SERIAL PRIMARY KEY,
    client_id int REFERENCES clients(id),
    email VARCHAR(40) UNIQUE,
    phone INTEGER);
    ''')
    conn.commit()


def add_client(conn, first_name, last_name, email, phones=None):
    cur.execute('''
    INSERT INTO clients(first_name, last_name) values(%s, %s) returning id;
     ''', (first_name, last_name))
    conn.commit
    client_id = cur.fetchone()
    cur.execute('''
    INSERT INTO client_info(email, phone, client_id) values(
    %s, %s, %s  );
     ''', (email, phones, client_id))
    conn.commit()


def add_phone(conn, client_id, phone):
    cur.execute("""
    UPDATE client_info SET phone=%s WHERE client_id=%s;
    """, (phone, client_id))
    conn.commit()


def change_client(conn, client_id, first_name=None, last_name=None, email=None, phones=None):
    cur.execute("""
    UPDATE clients SET first_name=%s, last_name=%s WHERE id=%s returning id;
    """, (first_name, last_name, client_id))
    conn.commit()
    cur.execute("""
    UPDATE client_info SET email=%s, phone=%s WHERE client_id=%s;
    """, (email, phones, client_id))
    conn.commit()


def delete_phone(conn, client_id, phone):
    cur.execute("""
    DELETE FROM client_info WHERE client_id=%s and phone=%s;""", (client_id, phone))
    conn.commit()


def delete_client(conn, client_id):
    cur.execute("""
    DELETE FROM client_info WHERE client_id=%s;""", (client_id))
    conn.commit()
    cur.execute("""
    DELETE FROM clients WHERE id=%s;""", (client_id))
    conn.commit()


def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    cur.execute("""
    SELECT c.id, first_name, last_name, email, phone FROM clients as c  
    left join client_info as ci on c.id=ci.client_id
    WHERE first_name=%s or last_name=%s or email=%s or phone=%s;""", (first_name, last_name, email, phone))
    client_info = cur.fetchall()[0]
    ID = client_info[0]
    FIRST_NAME = client_info[1]
    LAST_NAME = client_info[2]
    EMAIL = client_info[3]
    PHONE = client_info[4]
    return f'ID: {ID} | FIRST_NAME: {FIRST_NAME} | LAST_NAME: {LAST_NAME} | EMAIL: {EMAIL} | PHONE: {PHONE}'

with psycopg2.connect(database="clients_db", user="postgres", password="postgres") as conn:
    with conn.cursor() as cur:
        create_db(conn)
        add_client(conn=conn, first_name="Sava", last_name="Chernyak", email='vachernyak@mts.ru', phones=None)
        add_client(conn=conn, first_name="Vov", last_name="Ton", email='wer@wer.ru', phones=3333)
        add_phone(conn=conn, client_id=1, phone=44444)
        change_client(conn=conn, client_id=2, first_name='Bob', last_name='Marly')
        delete_phone(conn=conn, client_id=1, phone='44444')
        delete_client(conn=conn, client_id='1')
        print(find_client(conn=conn, first_name='Sava'))
conn.close()
