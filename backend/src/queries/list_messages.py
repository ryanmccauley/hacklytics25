from pydantic import BaseModel
from models.entities import ChatMessage, Challenge
from typing import List
from mediator import mediator
from database.mongo import engine
from odmantic import ObjectId
from fastapi import HTTPException


class ListMessagesQuery(BaseModel):
    challenge_id: str


class ListMessagesQueryResponse(BaseModel):
    messages: List[ChatMessage]


@mediator.register_handler(ListMessagesQuery)
async def list_messages(query: ListMessagesQuery):
    challenge = await engine.find_one(
        Challenge, Challenge.id == ObjectId(query.challenge_id)
    )
    if challenge is None:
        raise HTTPException(status_code=404)

    messages = await engine.find(
        ChatMessage,
        ChatMessage.challenge_id == ObjectId(query.challenge_id),
        sort=ChatMessage.created_at.asc(),
    )

    return ListMessagesQueryResponse(messages=messages)
