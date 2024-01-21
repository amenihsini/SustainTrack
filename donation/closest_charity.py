
#donation.py
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, String, Float, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import List
from geopy.geocoders import Nominatim
from fastapi import FastAPI, HTTPException, Depends
from fastapi import Query
from fastapi.middleware.cors import CORSMiddleware


# FastAPI App Initialization
app = FastAPI()

# CORS Configuration
origins = ["http://localhost:8080"]  # Replace with the actual address of your Vue.js app
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

# Charity Model
class Charity(Base):
    __tablename__ = "charities"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    address = Column(String(100), nullable=False)
    contact_info = Column(String(50), nullable=False)
    latitude = Column(Float)
    longitude = Column(Float)

# Create tables
Base.metadata.create_all(bind=engine)

# Pydantic Model for Request
class CharityCreate(BaseModel):
    name: str
    address: str
    contact_info: str

# Pydantic Model for Response
class CharityResponse(BaseModel):
    id: int
    name: str
    address: str
    contact_info: str
    latitude: float
    longitude: float

# Calculate Haversine Distance
def calculate_haversine_distance(coord1, coord2):
    if None in coord1 or None in coord2:
        return float('inf')

    return ((coord1[0] - coord2[0]) ** 2 + (coord1[1] - coord2[1]) ** 2) ** 0.5

# Sort charities by distance
def sort_charities_by_distance(charities):
    return sorted(charities, key=lambda x: x.distance)



# FastAPI Endpoints
@app.post("/charities", response_model=CharityResponse)
def add_charity(charity: CharityCreate, db: Session = Depends(get_db)):
    try:
        geolocator = Nominatim(user_agent="sustain_track")
        location = geolocator.geocode(charity.address)

        if location:
            latitude, longitude = location.latitude, location.longitude
        else:
            latitude, longitude = None, None

        new_charity = Charity(
            name=charity.name,
            address=charity.address,
            contact_info=charity.contact_info,
            latitude=latitude,
            longitude=longitude,
        )

        db.add(new_charity)
        db.commit()
        db.refresh(new_charity)

        return new_charity

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/charities", response_model=List[CharityResponse])
def get_charities(db: Session = Depends(get_db)):
    try:
        all_charities = db.query(Charity).all()
        charities_response = []

        for charity in all_charities:
            latitude = charity.latitude if charity.latitude is not None else 0.0
            longitude = charity.longitude if charity.longitude is not None else 0.0

            charity_response = CharityResponse(
                id=charity.id,
                name=charity.name,
                address=charity.address,
                contact_info=charity.contact_info,
                latitude=latitude,
                longitude=longitude
            )
            charities_response.append(charity_response)

        return charities_response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Modify the Query import statement
from fastapi import Query

@app.get("/charities/closest", response_model=List[CharityResponse])
def get_closest_charities(user_address: str = Query(...), db: Session = Depends(get_db)):
    try:
        geolocator = Nominatim(user_agent="your_app_name")
        location = geolocator.geocode(user_address)

        if location:
            user_location = location.latitude, location.longitude
        else:
            user_location = None, None

        all_charities = db.query(Charity).all()

        for charity in all_charities:
            distance = calculate_haversine_distance(user_location, (charity.latitude, charity.longitude))
            setattr(charity, "distance", distance)

        # Sort the charities based on distance before returning
        sorted_charities = sorted(all_charities, key=lambda x: x.distance)

        closest_charities = sorted_charities[:5]  # Adjust the number as needed

        return closest_charities

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8888)
