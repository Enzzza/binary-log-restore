from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

db_user = 'root'
db_pass = 'password'
db_addr = 'localhost'
db_name = 'smartmate'

url = f"mysql+pymysql://{db_user}:{db_pass}@{db_addr}/{db_name}"
engine = create_engine(url, echo=True)

# Create database if it does not exist.
if not database_exists(engine.url):
    create_database(engine.url)
else:
    # Connect the database if exists.
    engine.connect()