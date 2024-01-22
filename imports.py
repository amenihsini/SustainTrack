from datetime import datetime, date, timedelta
from uuid import uuid4
from typing import List, Union, Dict
from sqlalchemy import create_engine, Column, String, Float, Date, Integer, ForeignKey, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from fastapi import FastAPI, Depends, HTTPException, Path, Body
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2AuthorizationCodeBearer

from models import Product, Transaction, Base 
from database import create_app

import uvicorn
