import os

from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker, declarative_base

from dotenv import load_dotenv

load_dotenv()

def require_env(name: str) -> str:
    value = os.getenv(name)
    if value is None:
        raise RuntimeError(f"Variable d'environnement manquante : {name}")
    return value


SQLALCHEMY_DATABASE_URL = URL.create(
    drivername="postgresql+psycopg",
    username=require_env("POSTGRES_USER"),
    password=require_env("POSTGRES_PASSWORD"),
    host=require_env("POSTGRES_HOST"),
    port=int(require_env("POSTGRES_PORT")),
    database=require_env("POSTGRES_DB"),
)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"connect_timeout": 5},
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()