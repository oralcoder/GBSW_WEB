import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def get_connection():
	return psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host="db",  # docker-compose 서비스 이름
        port=os.getenv("POSTGRES_PORT"),
)