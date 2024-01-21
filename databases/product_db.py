# database.py
from typing import Tuple
from fastapi import FastAPI, Depends
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import sessionmaker, Session
from models import Base, Product  # Import Product

def create_app() -> Tuple[FastAPI, DeclarativeMeta]:
    app = FastAPI()

    # Set up SQLAlchemy
    database_url = 'sqlite:///products.db'
    engine = create_engine(database_url)
    Base.metadata.create_all(bind=engine)

    # Create SessionLocal
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    def get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = get_db

    return app, engine

