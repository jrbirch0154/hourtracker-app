# test_main.py
# Wed Sep 16 21:52:27 2026
# Jacob Birch

"""
This file tests main.py
"""

# %% Initializing

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Base
from main import app, get_db


@pytest.fixture
def client(tmp_path):
    """
    Test client wired to a brand-new, empty database
    """

    engine = create_engine(f"sqlite:///{tmp_path / 'test.db'}",
                           connect_args={"check_same_thread": False})

    TestSession = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)

    def get_test_db():
        db = TestSession()

        try:
            yield db

        finally:
            db.close()

    app.dependency_overrides[get_db] = get_test_db
    yield TestClient(app)

    app.dependency_overrides.clear()
    engine.dispose()


def make_entry(client, **changes):
    """
    Create an entry with defaults and return the JSON
    """

    data = {"project": "test",
            "date": "2000-12-27",
            "minutes": 65,
            "notes": "just a test"}

    data.update(changes)
    response = client.post("/entries", json=data)
    assert response.status_code == 200
    return response.json()


def test_update_saves(client):
    entry = make_entry(client)

    client.patch(f"/entries/{entry['id']}", json={"project": "renamed_test"})

    assert client.get(
        f"/entries/{entry['id']}").json()['project'] == "renamed_test"


def test_delete(client):
    entry = make_entry(client)

    response = client.delete(f"/entries/{entry['id']}")

    assert response.status_code == 200
    assert client.get(f"/entires/{entry['id']}").status_code == 404
    
    
def test_no_entries_exist(client):
    
    response = client.get("/entries")
    
    assert response.status_code == 200
    assert response.json() == []
