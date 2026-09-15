import psycopg2
from config import load_config
from commands import commands

def generate_db():

    config = load_config()

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor as cur:

                for command in commands:
                    cur.execute(command)

            conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)