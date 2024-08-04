from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os.path
file_dir = os.path.abspath(__file__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_dir = os.path.join(BASE_DIR,'../scrap01.db')
print(f"db_address = {db_dir}")

SQLALCHEMY_DATABASE_URL = f"sqlite:///{db_dir}"
# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}  # is needed only for SQLite
)

Base = declarative_base()
from  .pte_db import *
Base.metadata.create_all(engine, checkfirst=True)
print('create tables...')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#
#
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import scoped_session, sessionmaker
#
# DBSession = scoped_session(sessionmaker())
# Base = declarative_base()
#
# def initialize_sql(engine):
#     DBSession.configure(bind=engine)
#     Base.metadata.bind = engine
#     Base.metadata.create_all(engine)
