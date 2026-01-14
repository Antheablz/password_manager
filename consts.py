
USERNAME = 'postgres'
PASSWORD = '9210'
HOST = 'localhost'
PORT = '5432'
DB_DEFAULT = 'postgres'
DB_PM = 'password_manager_db'

DEFAULT_DB_URL = f'postgresql+psycopg2://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DB_DEFAULT}'
PM_DB_URL = f'postgresql+psycopg2://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DB_PM}'

PWD_TABLE_NAME = "passwords"

TABLE_WIDTH = 55
TABLE_HEIGHT = 30