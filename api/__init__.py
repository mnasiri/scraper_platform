from fastapi import FastAPI

from database import SessionLocal, Base as DBBase, engine

DBBase.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Basic routing with an HTTP GET method to return a welcome message
@app.get("/")
async def home():
    return {"message": "Welcome to scrapper platform API!"}

from api.pte_api import *
