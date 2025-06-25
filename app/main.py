from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
import uvicorn

app = FastAPI()

@app.get("/blog")
async def index(limit=10, pusblished: bool = True, sort: Optional[str]=None):
    if pusblished:
        return {"data": f" published {pusblished}"}
    else:
         return {"data": f" limit {limit}"}

@app.get("/blog/unpublished")
def unpublished():
    return { "data": {"unpublished": "all unpublished"}}
    

@app.get("/blog/{id}")
def read_item(id: int):
    return {"data": {"id": id}}

class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool]

@app.post("/blog")
 
def create_blog(request: Blog):
    return {"data": f"The blog title is {request.title}"}


# DEBUGING PURPOSE ONLY
# if __name__=="__main__":
#     uvicorn.run(app, host="127.0.0.1", port=3000)