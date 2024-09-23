import os
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker


load_dotenv()

engine = create_engine(os.getenv('DATABASE_URL'))  # создание объекта "движка" для подключения к базе данных и выполнения SQL-запросов через SQLAlchemy
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)  # создание фабрики сессий для выполнения операций с базой данных 
Base = declarative_base() # создание базового класса, от которого будут наследоваться все модели базы данных

def get_db():
    """Подключение к базе данных"""
    db = SessionLocal()   # создание новой сессии базы данных
    try:
        yield db
    finally:
        db.close()





