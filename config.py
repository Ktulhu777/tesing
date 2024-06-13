import os
from dotenv import load_dotenv

load_dotenv()

host = os.environ.get("host")
access_key = os.environ.get("access_key")
secret_key = os.environ.get("secret_key")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
