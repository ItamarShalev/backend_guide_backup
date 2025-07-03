from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {
        "status": True,
        "message": "Hello from backend-guide!"
    }
