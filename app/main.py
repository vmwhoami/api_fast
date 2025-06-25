from typing import Annotated
from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel,create_engine, select

# — Your SQLModel Training class unchanged —
class Training(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    age: int | None = Field(default=None, index=True)
    duration: str

# — DB setup and session dependency unchanged — #
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

def get_session():
    with Session(engine) as session:
        yield session

session = Annotated[Session, Depends(get_session)]

# — Replace on_event with lifespan — #
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup block
    SQLModel.metadata.create_all(engine)
    yield
    # Shutdown block (optional cleanup)
    # e.g., dispose engine or close connections

app = FastAPI(lifespan=lifespan)

# — Your routes stay the same — #
@app.post("/trainig_session/")
def create_session(training: Training, session: session) -> Training:
    session.add(training); session.commit(); session.refresh(training)
    return training

@app.get("/trainig_session/")
def read_trainig_session(session: session, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100,) -> list[Training]:
    return session.exec(select(Training).offset(offset).limit(limit)).all()

@app.get("/trainig_session/{session_id}")
def read_session(session_id: int, session: session) -> Training:
    training = session.get(Training, session_id)
    if not training:
        raise HTTPException(status_code=404, detail="Training not found")
    return training

@app.delete("/trainig_session/{session_id}")
def delete_hero(session_id: int, session: session):
    training = session.get(Training, session_id)
    if not training:
        raise HTTPException(status_code=404, detail="Training not found")
    session.delete(training); session.commit()
    return {"ok": True}
