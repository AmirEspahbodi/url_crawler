import os
from app.core.config import PostgresConfig
import psycopg2

# establishing the connection
conn = psycopg2.connect(
    database="postgres",
    user="postgres",
    password="postgres",
    host="URL_CRAWLER_DB",
    port="5432",
)
conn.autocommit = True

# Creating a cursor object using the cursor() method
cursor = conn.cursor()

# check 'url_crawler' database exists
cursor.execute("SELECT datname FROM pg_database")
database_records = [row[0] for row in cursor.fetchall()]

url_crawler_exist = "url_crawler" in database_records


# create url_crawler database if not exist
if not url_crawler_exist:
    cursor.execute("CREATE DATABASE url_crawler")
    print("url_crawler database created")

conn.close()


# make migration
os.system('alembic revision --autogenerate -m "New Migration"')

# migrate
os.system("alembic upgrade head")
