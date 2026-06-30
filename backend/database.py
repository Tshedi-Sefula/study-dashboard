# Database configurations
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# PostGres allows multiple db connections without errors thrown
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# usng engine object to create a session
# session points to engine, and adds more settings
SessionRemote = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base() # for the models in model.py


