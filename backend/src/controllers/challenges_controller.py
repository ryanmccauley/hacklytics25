from fastapi import APIRouter, HTTPException, Depends
from database.mongo import engine
from models.entities import Challenge
from models.web_models import CreateChallengeRequest
from commands.create_challenge import CreateChallengeCommand, CreateChallengeResponse
from mediator import Mediator, get_mediator

challenges_router = APIRouter(prefix="/challenges")

@challenges_router.get("/{id}")
async def get_challenge(id: str):
  challenge = await engine.find_one(Challenge, Challenge.id == id)

  if challenge is None:
    raise HTTPException(status_code=404)

  return challenge

@challenges_router.post("/")
async def create_challenge(
  request: CreateChallengeRequest,
  mediator: Mediator[CreateChallengeCommand, CreateChallengeResponse] = Depends(get_mediator)
):
  command = CreateChallengeCommand(
    category=request.category,
    difficulty=request.difficulty,
    additional_prompt=request.additional_prompt
  )

  response = await mediator.send(command)

  return { "id": response.challenge_id }

@challenges_router.post("/{id}/completions")
async def create_challenge_chat_completion(id: str):
  challenge = await engine.find_one(Challenge, Challenge.id == id)

  if challenge is None:
    raise HTTPException(status_code=404)

  pass