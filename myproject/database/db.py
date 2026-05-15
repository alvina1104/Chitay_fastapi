from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,DeclarativeBase
from sqlalchemy.ext.declarative import declarative_base

DB_URL = 'postgresql://postgres:admin@localhost:5433/chitay_app_vin11'
engine = create_engine(DB_URL)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()
