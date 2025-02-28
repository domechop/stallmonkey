import pytest
import os
import tempfile
from app_dir.app import app
from app_dir.database import init_db


@pytest.fixture
def client():
    # Create a temporary file to isolate the database for tests
    db_fd, db_path = tempfile.mkstemp()
    app.config["DATABASE"] = db_path
    app.config["TESTING"] = True

    # Initialize the test database
    with app.app_context():
        init_db()

    with app.test_client() as client:
        yield client

    # Close and remove the temporary file
    os.close(db_fd)
    os.unlink(db_path)


def test_home_page(client):
    """Test that home page loads successfully"""
    rv = client.get("/")
    assert rv.status_code == 200


def test_permits_page(client):
    """Test that permits page loads successfully"""
    rv = client.get("/permits")
    assert rv.status_code == 200


def test_school_info_page(client):
    """Test that school info page loads successfully"""
    rv = client.get("/school_info")
    assert rv.status_code == 200


def test_invalid_permit_checkout(client):
    """Test accessing an invalid permit ID"""
    rv = client.get("/checkout/999999")
    assert b"Permit not found!" in rv.data
