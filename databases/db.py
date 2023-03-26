import psycopg2

connection = psycopg2.connect(
    host='localhost',
    user='postgres',
    password='1234',
    database='postgres'
)

connection.autocommit = True


def create_table_users():
    with connection.cursor() as cursor:
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS users(
                id serial,
                vk_id varchar(20) NOT NULL);"""
        )

def create_table_showed_users():
    with connection.cursor() as cursor:
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS showed_users(
            id serial,
            vk_id varchar(20) NOT NULL);"""
        )

def insert_users(vk_id):
    with connection.cursor() as cursor:
        cursor.execute(
            f"""INSERT INTO users (vk_id)
            VALUES ('{vk_id}');"""
        )


def insert_showed_users(vk_id):
    with connection.cursor() as cursor:
        cursor.execute(
            f"""INSERT INTO showed_users (vk_id)
            VALUES ('{vk_id}');"""
        )

def drop_users():
    with connection.cursor() as cursor:
        cursor.execute(
            """DROP TABLE IF EXISTS users CASCADE;"""
        )

def creating_database():
    drop_users()
    create_table_users()
    create_table_showed_users()
