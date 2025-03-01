import os

# get environment variables and set them as constants
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")

URL_HAMSTER = os.getenv("URL_HAMSTER")
# URL_CHAMELEON = os.getenv("URL_CHAMELEON")
