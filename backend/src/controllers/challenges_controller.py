from fastapi import APIRouter

challenges_router = APIRouter(prefix="/challenges")

@challenges_router.get("/{id}")
async def get_challenge(id: str):
  pass

@challenges_router.post("/")
async def create_challenge():
  pass

@challenges_router.post("/{id}/completions")
async def create_challenge_chat_completion(id: str):
  pass