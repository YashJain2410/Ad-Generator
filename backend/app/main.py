from fastapi import FastAPI
from .routers import auth

from .db.session import engine
from .models import user

app = FastAPI(title="AI Ad Generator API")

@app.get("/")
def root():
    return {"message" : "API Running"}

app.include_router(auth.router)

user.Base.metadata.create_all(bind=engine)