from fastapi import FastAPI
from routes import ai_routes

app = FastAPI()

app.include_router(ai_routes.router)

@app.get("/")
def main():
  return {"Hello": "World"}
