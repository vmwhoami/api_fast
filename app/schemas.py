 
from fastapi import Depends, FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import Optional
from sqlmodel import Field, Session, SQLModel, create_engine, select
class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool]