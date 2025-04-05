import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = 'your-secret-key-here'
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'             # Default XAMPP username
    MYSQL_PASSWORD = ''             # Default XAMPP password is empty
    MYSQL_DB = 'appointtrack'       # Must match your database name