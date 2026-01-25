from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.getenv("DATABASE_HOST")
DB_PORT = os.getenv("DATABASE_PORT")
DB_NAME = os.getenv("DATABASE_NAME")
DB_USER = os.getenv("DATABASE_USER")
DB_PASS = os.getenv("DATABASE_PASS")

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

DB_CONFIG = {
    "database" : DB_NAME,
    "user" : DB_USER,
    "port" : DB_PORT,
    "host" : DB_HOST,
    "password" : DB_PASS
}
