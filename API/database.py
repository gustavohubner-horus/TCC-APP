from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from dotenv import load_dotenv
import os

load_dotenv()

URL_BANCO = os.getenv("URL_BANCO")

engine = create_engine(URL_BANCO)
SessionLocal = sessionmaker(bind=engine)
class Base(DeclarativeBase): pass


# controla a sessão do banco 
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()