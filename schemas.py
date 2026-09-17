# schemas.py
# Wed Sep 16 18:26:33 2026
# Jacob Birch

"""
This will house the pydantic models (request + response)
"""

# %% Initializing

from pydantic import BaseModel, ConfigDict
import datetime


class EntryIn(BaseModel):
    """
    This is what the client is allowed to send. It sets the shape of incoming JSON or POST
    """
    project: str
    date: datetime.date
    minutes: float
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
