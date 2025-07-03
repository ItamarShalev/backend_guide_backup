from fastapi import FastAPI

from src.db.database import engine
from src.db.models import Base
from src.routers import auth, todos

Base.metadata.create_all(bind=engine)

app = FastAPI(name="backend-guide")
app.include_router(auth.router)
app.include_router(todos.router)


@app.get("/")
def root():
    return {"status": True, "message": "Hello from backend-guide!"}
