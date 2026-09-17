# schemas.py
# Wed Sep 16 18:26:33 2026
# Jacob Birch

"""
This will house the pydantic models (request + response).
Basically, ensures that the data coming in is correct
"""

# %% Initializing

from pydantic import BaseModel, ConfigDict, Field
import datetime


class EntryIn(BaseModel):
    """
    This is what the client is allowed to send. It sets the shape of incoming JSON or POST
    """
    project: str
    date: datetime.date
    minutes: float = Field(gt=0) # Greater Than 0
    notes: str | None = None


class EntryOut(EntryIn):
    """
    This is the shape of the outgoing JSON. What is being sent back.
    """
    id: int

    model_config = ConfigDict(from_attributes=True)


class SummaryOut(BaseModel):
    """
    Project's total logged time
    """

    project: str
    total_minutes: float

    model_config = ConfigDict(from_attributes=True)


class EntryUpdate(BaseModel):
    """
    Update a current entry
    """
    project: str | None = None
    date: datetime.date | None = None
    minutes: float | None = Field(default=None, gt=0)
    notes: str | None = None