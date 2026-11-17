import os

from dotenv import load_dotenv
from models.scans import Documents  # noqa: F401
from models.user import User  # noqa: F401
from sqlmodel import Session, SQLModel, create_engine
from supabase import Client, create_client

load_dotenv()


engine = create_engine(os.environ.get("DATABASE_URL"))
SQLModel.metadata.create_all(engine)


def getSession():
    with Session(engine) as session:
        yield session


supabase: Client = create_client(
    os.environ.get("SUPABASE_URL"), os.environ.get("SUPABASE_KEY")
)
