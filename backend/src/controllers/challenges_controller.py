from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import StreamingResponse
from database.mongo import engine
from models.entities import Challenge
from models.web_models import CreateChallengeRequest
from commands.create_challenge import CreateChallengeCommand, CreateChallengeResponse
from mediator import Mediator, get_mediator
from odmantic import ObjectId
from queries.get_challenge import GetChallengeQuery, GetChallengeQueryResponse
from commands.create_challenge_download import CreateChallengeDownloadCommand, CreateChallengeDownloadResponse

challenges_router = APIRouter(prefix="/challenges")

@challenges_router.get("/{id}")
async def get_challenge(
  id: str,
  mediator: Mediator[GetChallengeQuery, GetChallengeQueryResponse] = Depends(get_mediator)
):
  query = GetChallengeQuery(challenge_id=id)
  response = await mediator.send(query)

  if response.challenge is None:
    raise HTTPException(status_code=404)

  return response.challenge

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

@challenges_router.get("/{id}/download")
async def create_challenge_download(
  id: str,
  mediator: Mediator[CreateChallengeDownloadCommand, CreateChallengeDownloadResponse] = Depends(get_mediator)
):
  command = CreateChallengeDownloadCommand(challenge_id=id)
  response = await mediator.send(command)

  return StreamingResponse(response.file_contents, media_type="application/zip")

@challenges_router.post("/{id}/completions")
async def create_challenge_chat_completion(id: str):
  challenge = await engine.find_one(Challenge, Challenge.id == id)

  if challenge is None:
    raise HTTPException(status_code=404)

  pass