from fastapi import FastAPI
from controllers.challenges_controller import challenges_router
import uvicorn

app = FastAPI()

app.include_router(challenges_router)

uvicorn.run(app, host="0.0.0.0", port=8000)