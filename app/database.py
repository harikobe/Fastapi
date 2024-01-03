from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
#import the config file
from .config import settings

#URL of database(Postgres SQL )
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

#creating the engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

#creating the session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#creating the Base
Base = declarative_base()


#creating an db session using SessionLocal:
#its an concept of dependencies with yield:
def get_db():
     db=SessionLocal()
     try:
          yield db
     finally:
          db.close()


"""
    just for documentation
#-------------------------------------------------------------------------------------
for this:
import psycopg2
from psycopg2.extras import RealDictCursor
import time
#random package fro to create random number 
from random import randrange

#database connection:
while True:
     
     try:
         conn=psycopg2.connect(
              host="localhost",
              database="Fastapi-dev",
              user="postgres",
              password="harik1234",
              cursor_factory=RealDictCursor
              )
         
         #used for query statements:
         cursor = conn.cursor()
         print("Database connection was successful")
         break
     except Exception as error:
         print("Connecting to Database Failed")
         print("Error:",error)
         time.sleep(2)

#------------------------------------------------------------------------------------

"""