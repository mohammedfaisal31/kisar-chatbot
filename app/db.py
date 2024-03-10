from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv
from models import Base  

load_dotenv()

host = os.getenv("DB_HOST")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
database = os.getenv("DB_NAME")

# MySQL Connector connection string
connection_string = f"mysql+mysqlconnector://{user}:{password}@{host}/{database}"

# Create SQLAlchemy engine
engine = create_engine(connection_string)

# Create the database schema
Base.metadata.create_all(engine)

# Create a sessionmaker
Session = sessionmaker(bind=engine)

# Perform query using the model
def get_db():
    with Session() as session:
        return session
