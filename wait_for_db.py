import time
import psycopg2
from django.db.utils import OperationalError
import os
import environ
from pathlib import Path
env = environ.Env()
environ.Env.read_env()
def wait_for_db():
    retries = 5
    db_ready = False
    while not db_ready:
        try:
            conn = psycopg2.connect(
                dbname=os.getenv('POSTGRES_DB'),
                user=os.getenv('POSTGRES_USER'),
                password=os.getenv('POSTGRES_PASSWORD'),
                host="db",  # Название контейнера с БД
                port="5432"
            )
            db_ready = True
            conn.close()
        except OperationalError:
            print("База данных не готова, ждем...")
            time.sleep(2)

wait_for_db()