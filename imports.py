from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime, date, timedelta
from uuid import uuid4
from pydantic import BaseModel
from models import Product, Transaction
from database import create_app
from typing import List
from sqlalchemy import create_engine
import uvicorn
from fastapi.responses import PlainTextResponse
from fastapi import HTTPException, Path, Body
from typing import Union, Dict, List
from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship
from models import Base, Product 
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from sqlalchemy import Column, String, Float, Date, Integer, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship

