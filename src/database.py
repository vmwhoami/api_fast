from fastapi import Depends, FastAPI, HTTPException, Query
from typing import Annotated
from sqlmodel import Field, Session, SQLModel,create_engine, select

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

def get_session():
    with Session(engine) as session:
        yield session

session = Annotated[Session, Depends(get_session)]