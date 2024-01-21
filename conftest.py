# conftest.py
from app import engine

def pytest_sessionfinish(session, exitstatus):
    # This fixture will dispose of the engine, ensuring the SQLite database is closed after tests
    engine.dispose()
