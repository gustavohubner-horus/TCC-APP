from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

URL_BANCO = os.getenv("URL_BANCO")

engine = create_engine(URL_BANCO)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()