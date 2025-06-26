from datetime import datetime, timezone
from uuid import uuid4, UUID
from sqlalchemy.orm import Session
from fastapi import HTTPException
from . import model
from src.auth.model import TokenData
from src.entities.todo import Todo
from src.exceptions import TodoCreationError, TodoNotFoundError
import logging

def create_todo(current_user: TokenData, db: Session, todo: model.TodoCreate) -> Todo:
    try:
        new_todo = Todo(**todo.model_dump())
        new_todo.user_id = current_user.user_id
        db.add(new_todo)
        db.commit()
        db.refresh(new_todo)
        logging.info(f"Created new todo for user: {current_user.user_id}")
        return new_todo
    except Exception as e:
        logging.error(f"Failed to create todo for user {current_user.user_id}. Error: {str(e)}")
        db.rollback()
        raise TodoCreationError(str(e))

def get_todos(current_user: TokenData, db: Session) -> list[model.TodoResponse]:
    todos = db.query(Todo).filter(Todo.user_id == current_user.user_id).all()
    logging.info(f"Retrieved {len(todos)} todos for user: {current_user.user_id}")
    return todos