from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers.challenges_controller import challenges_router
import uvicorn

app = FastAPI()

app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

app.include_router(challenges_router)

uvicorn.run(app, host="0.0.0.0", port=8000)