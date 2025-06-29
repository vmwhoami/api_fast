from fastapi import FastAPI
from .database.core import engine, Base
from .entities.todo import Todo 
from .entities.user import User 
from .api import register_routes
import os
from .logging import configure_logging, LogLevels
from dotenv import load_dotenv
load_dotenv()

configure_logging(LogLevels.info)
app = FastAPI()

""" Only uncomment below to create new tables,
otherwise the tests will fail if not connected
"""
# Auto-create tables only in development
# if os.getenv("ENVIRONMENT", "production") == "development":
# Base.metadata.create_all(bind=engine)

register_routes(app)