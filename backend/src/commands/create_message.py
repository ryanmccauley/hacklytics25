from mediator import mediator, MediatorDTO
from models.entities import Challenge, ChatMessage
from database.mongo import engine
from odmantic import ObjectId
from typing import Literal
from fastapi import HTTPException
from datetime import datetime

class CreateMessageCommand(MediatorDTO):
  challenge_id: str
  content: str
  role: Literal["user", "assistant"]

class CreateMessageCommandResponse(MediatorDTO):
  message: ChatMessage

@mediator.register_handler(CreateMessageCommand)
async def create_message(command: CreateMessageCommand):
  challenge = await engine.find_one(Challenge, Challenge.id == ObjectId(command.challenge_id))
  if challenge is None:
    raise HTTPException(status_code=404)

  message = ChatMessage(
    id=ObjectId(),
    challenge_id=ObjectId(command.challenge_id),
    content=command.content,
    role=command.role,
    created_at=datetime.utcnow()
  )

  await engine.save(message)

  return CreateMessageCommandResponse(message=message)