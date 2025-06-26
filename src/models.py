from sqlalchemy import Column, Integer, String
from sqlmodel import Field, Session, SQLModel,create_engine, select
from .database import Base
class Training(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    age: int | None = Field(default=None, index=True)
    duration: Integer