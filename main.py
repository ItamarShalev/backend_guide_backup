from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.db.database import engine
from src.db.models import Base
from src.routers import auth, todos
from src.utils import Utils

environment = Utils.environment()

Base.metadata.create_all(bind=engine)

app = FastAPI(name="backend-guide")
app.include_router(auth.router)
app.include_router(todos.router)

if environment.DEVELOPMENT:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.get("/")
def root():
    return {"status": True, "message": "Hello from backend-guide!"}
