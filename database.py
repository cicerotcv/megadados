from dotenv import dotenv_values
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists
from sqlalchemy_utils.functions.database import create_database

env = dict(dotenv_values('.env'))

DATABASE_URL = env.get("DB_URL")

if not DATABASE_URL:
    raise Exception("A variável de ambiente DB_URL não foi carregada adequadamente. Verifique  file.")


engine = create_engine(DATABASE_URL)

if not database_exists(engine.url):
    print("Database não existia")
    create_database(engine.url)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


Base = declarative_base()
