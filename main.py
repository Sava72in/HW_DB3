import psycopg2


def create_db(conn):
    cur.execute('''
    CREATE TABLE IF NOT EXISTS clients(
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(30) NOT NULL,
    last_name VARCHAR(30) NOT NULL,
    email VARCHAR(40) UNIQUE);
     ''')
    conn.commit()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS client_info(
    id SERIAL PRIMARY KEY,
    client_id int REFERENCES clients(id),
    phone INTEGER);
    ''')
    conn.commit()


def add_client(conn, first_name, last_name, email, phones=None):
    cur.execute('''
    INSERT INTO clients(first_name, last_name, email) values(%s, %s, %s) returning id;
     ''', (first_name, last_name, email))
    conn.commit
    client_id = cur.fetchone()
    cur.execute('''
    INSERT INTO client_info(phone, client_id) values(
    %s, %s);
     ''', (phones, client_id))
    conn.commit()


def add_phone(conn, client_id, phone):
    cur.execute("""
    INSERT INTO client_info(phone, client_id) values(
    %s, %s);""", (phone, client_id))
    conn.commit()


def change_client(conn, client_id, first_name=None, last_name=None, email=None, phones=None):
    sql_query = "UPDATE clients SET "
    update_params = []
    if first_name is not None:
        sql_query += "first_name = %s, "
        update_params.append(first_name)
    if last_name is not None:
        sql_query += "last_name = %s, "
        update_params.append(last_name)
    if email is not None:
        sql_query += "email = %s, "
        update_params.append(email)
    sql_query = sql_query.rstrip(", ")
    sql_query += " WHERE id = %s"
    update_params.append(client_id)
    cur.execute(sql_query, update_params)
    if phones is not None:
        sql_query = "UPDATE client_info SET "
        sql_query += "phone = %s"
        sql_query += " WHERE client_id = %s"
        cur.execute(sql_query, (phones, client_id))
    conn.commit()


def delete_phone(conn, client_id, phone):
    cur.execute("""
    DELETE FROM client_info WHERE client_id=%s and phone=%s;""", (client_id, phone))
    conn.commit()


def delete_client(conn, client_id):
    cur.execute("""
    DELETE FROM client_info WHERE client_id=%s;""", client_id)
    conn.commit()
    cur.execute("""
    DELETE FROM clients WHERE id=%s;""", client_id)
    conn.commit()


def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    sql_query = "SELECT c.id ,c.first_name ,c.last_name , c.email ,ci.phone " \
                "FROM clients c left join client_info ci on c.id = ci.client_id where  "
    find_params = []
    if first_name is not None:
        sql_query += "c.first_name = %s and "
        find_params.append(first_name)
    if last_name is not None:
        sql_query += "c.last_name = %s and "
        find_params.append(last_name)
    if email is not None:
        sql_query += "c.email = %s and "
        find_params.append(email)
    sql_query = sql_query.rstrip("and ")
    cur.execute(sql_query, find_params)
    print(cur.fetchall())
    if phone is not None:
        sql_query = """SELECT c.id ,c.first_name ,c.last_name , c.email ,ci.phone  FROM client_info ci 
                        left join clients c on c.id = ci.client_id 
                            where phone = %s """
        cur.execute(sql_query, (phone,))


if __name__ == '__main__':
    with psycopg2.connect(database="clients_db", user="postgres", password="postgres") as conn:
        with conn.cursor() as cur:
            create_db(conn)
            add_client(conn=conn, first_name="Sava", last_name="Chernyak", email='vachernyak@mts.ru', phones=None)
            add_client(conn=conn, first_name="Vov", last_name="Ton", email='wer@wer.ru', phones=3333)
            add_phone(conn=conn, client_id=2, phone=44444)
            change_client(conn=conn, client_id=2, first_name='Bob', last_name='Marly', email='test@test.test', phones=333)
            delete_phone(conn=conn, client_id=1, phone='44444')
            delete_client(conn=conn, client_id='1')
            print(find_client(conn=conn, first_name='Bob', phone=333))
    conn.close()
