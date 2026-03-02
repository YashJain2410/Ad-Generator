from fastapi import FastAPI
from .routers import auth
from .routers import brands
from .routers import projects
from .routers import assets

from .db.session import engine
from .models import user

app = FastAPI(title="AI Ad Generator API")

@app.get("/")
def root():
    return {"message" : "API Running"}

app.include_router(auth.router)
app.include_router(brands.router)
app.include_router(projects.router)
app.include_router(assets.router)

user.Base.metadata.create_all(bind=engine)