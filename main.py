# main.py
# Wed Sep 16 18:18:47 2026
# Jacob Birch
# Use uvicorn main:app --reload

"""
The main will house the FastAPI app + routing
"""

# %% Initializing

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select, func
import datetime
import models
import schemas
from database import engine, SessionLocal, Base


Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/entries", response_model=schemas.EntryOut)
def create_entry(entry: schemas.EntryIn, db: Session = Depends(get_db)):
    db_entry = models.TimeEntryDB(**entry.model_dump())
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry


@app.get("/entries", response_model=list[schemas.EntryOut])
def read_entries(db: Session = Depends(get_db)):
    """
    Returns every entry, newest date first
    """
    statement = select(models.TimeEntryDB).order_by(
        models.TimeEntryDB.date.desc())

    return db.scalars(statement).all()


@app.get("/entries/{entry_id}", response_model=schemas.EntryOut)
def read_entry(entry_id: int, db: Session = Depends(get_db)):
    """
    Returns one entry. 404 if it does not exist
    """
    entry = db.get(models.TimeEntryDB, entry_id)

    if entry is None:
        raise HTTPException(status_code=404, detail=f"Entry {entry_id} does not exist")

    return entry


@app.delete("/entries/{entry_id}", response_model=schemas.EntryOut)
def delete_entry(entry_id: int, db: Session = Depends(get_db)):
    """
    Deletes one entry based on the ID.
    """

    entry = db.get(models.TimeEntryDB, entry_id)

    if entry is None:
        raise HTTPException(status_code=404, detail=f"Entry {entry_id} does not exist")

    db.delete(entry)
    db.commit()

    return entry


@app.get("/summary", response_model=list[schemas.SummaryOut])
def read_summary(start: datetime.date | None = None,
                 end: datetime.date | None = None,
                 db: Session = Depends(get_db)):
    """ 
    Total minutes, optionally listed to a date range.
    """

    total = func.sum(models.TimeEntryDB.minutes).label("total_minutes")

    statement = select(models.TimeEntryDB.project, total)

    if start is not None:
        statement = statement.where(models.TimeEntryDB.date >= start)
    if end is not None:
        statement = statement.where(models.TimeEntryDB.date <= end)

    statement = statement.group_by(
        models.TimeEntryDB.project).order_by(total.desc())

    return db.execute(statement).all()


@app.patch("/entries/{entry_id}", response_model=schemas.EntryOut)
def update_entry(entry_id: int, update: schemas.EntryUpdate, db: Session = Depends(get_db)):
    """
    Update one of the entries, based on ID
    """
    entry = db.get(models.TimeEntryDB, entry_id)

    if entry is None:
        raise HTTPException(status_code=404, detail=f"Entry {entry_id} does not exist")

    for key, value in update.model_dump(exclude_unset=True).items():
        setattr(entry, key, value)

    db.commit()
    db.refresh(entry)

    return entry
