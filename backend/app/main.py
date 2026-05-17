from app.routes import auth
from fastapi import FastAPI
from app.database import engine
from app.models import Base
from app.routes import student

app = FastAPI()
app.include_router(student.router)
app.include_router(auth.router)
# Create tables
Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "API is running"}

