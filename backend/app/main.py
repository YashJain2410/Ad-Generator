from fastapi import FastAPI

app = FastAPI(title="AI Ad Generator API")

@app.get("/")
def root():
    return {"message" : "API Running"}