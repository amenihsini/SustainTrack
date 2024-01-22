#charities.py
from imports import *

# FastAPI App Initialization
app = FastAPI()

# Database Initialization
DATABASE_URL = "sqlite:///charities_db.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# SQLAlchemy Base
Base = declarative_base()

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5002)

