import os

from .database import DatabaseConnection


db_connection = DatabaseConnection(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST")
)

# get environment variables and set them as constants
URL_HAMSTER = os.getenv("URL_HAMSTER")
