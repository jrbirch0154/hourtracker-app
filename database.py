# database.py
# Wed Sep 16 18:22:56 2026
# Jacob Birch

"""
The database will house the DB connection setup, from the SQLite
"""
#%% Initializing

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./hours.db"
connect_args = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()