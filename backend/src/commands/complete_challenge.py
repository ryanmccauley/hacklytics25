from mediator import mediator, MediatorDTO
from models.entities import Challenge
from odmantic import ObjectId
from fastapi import HTTPException
from database.mongo import engine
from datetime import datetime

class CompleteChallengeCommand(MediatorDTO):
  flag: str
  challenge_id: ObjectId

@mediator.register_handler(CompleteChallengeCommand)
async def complete_challenge(command: CompleteChallengeCommand):
  challenge = await engine.find_one(Challenge, Challenge.id == command.challenge_id)
  if challenge is None:
    raise HTTPException(status_code=404)

  if challenge.flag_solution != command.flag:
    raise HTTPException(status_code=400, detail="Invalid flag")

  challenge.completed_at = datetime.utcnow()
  await engine.save(challenge)

  return challenge
