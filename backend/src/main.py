from fastapi import FastAPI
from models.web_models import CreateCTFRequest
import uvicorn

app = FastAPI()

@app.get("/")
def index():
  return { "message": "Hello World" }

@app.post("/ctf")
async def create_ctf(request: CreateCTFRequest):
  print(request)
  return { "message": "CTF created" }

uvicorn.run(app, host="0.0.0.0", port=8000)