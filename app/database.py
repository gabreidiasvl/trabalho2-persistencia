from sqlmodel import SQLModel, create_engine, Session
import os
from dotenv import load_dotenv

load_dotenv()

database_url = os.getenv("DATABASE_URL")

connect_args = {"check_same_thread": False} if "sqlite" in database_url else {}

engine = create_engine(database_url, echo=False, connect_args=connect_args)

def get_session():
    with Session(engine) as session:
        yield session