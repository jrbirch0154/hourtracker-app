# models.py
# Wed Sep 16 18:25:25 2026
# Jacob Birch

"""
This will house the SQLAlchemy models
"""

#%% Initializing

from sqlalchemy import Column, Integer, String, Float, Date
from database import Base


class TimeEntryDB(Base):
    """
    This defines the database table. Columns, types, primary key
    """
    __tablename__ = "entries"
    
    id = Column(Integer, primary_key=True, index=True)
    project = Column(String, index=True)
    date = Column(Date)
    minutes = Column(Float)
    notes = Column(String, nullable=True)