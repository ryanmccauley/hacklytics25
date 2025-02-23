from mediator import mediator, MediatorDTO
from models.web_models import ChatMessageRequest
from typing import List
from fastapi.responses import StreamingResponse
from fastapi import HTTPException
from settings import global_settings
from langchain_core.messages import AIMessage, HumanMessage, BaseMessage, SystemMessage
from langchain_openai import ChatOpenAI
from database.mongo import engine
from models.entities import Challenge, ChatMessage
from odmantic import ObjectId
from datetime import datetime
from prompts import CHALLENGE_CHAT_PROMPT
from langchain_core.prompts import PromptTemplate

class CreateChallengeChatCompletionCommand(MediatorDTO):
  challenge_id: str
  messages: List[ChatMessageRequest]

@mediator.register_handler(CreateChallengeChatCompletionCommand)
async def create_challenge_chat_completion(
  command: CreateChallengeChatCompletionCommand,
):
  challenge = await engine.find_one(Challenge, Challenge.id == ObjectId(command.challenge_id))
  if challenge is None:
    raise HTTPException(status_code=404)

  model = ChatOpenAI(model="gpt-4o", api_key=global_settings.OPENAI_API_KEY)
  system_prompt = PromptTemplate.from_template(CHALLENGE_CHAT_PROMPT).invoke({ "challenge": challenge.model_dump_json() })
  print(system_prompt.text)


  messages = format_messages(command.messages, SystemMessage(content=system_prompt.text))

  async def event_stream():
    content = ""

    async for chunk in model.astream(messages):
      content += chunk.content
      yield chunk.content

    message = ChatMessage(
      id=ObjectId(),
      challenge_id=ObjectId(command.challenge_id),
      content=content,
      role="assistant",
      created_at=datetime.utcnow()
    )

    await engine.save(message)

  return StreamingResponse(event_stream(), media_type="text/event-stream")

def format_messages(messages: List[ChatMessageRequest], system_message: SystemMessage) -> List[BaseMessage]:
  formatted_messages = [system_message]

  for message in messages:
    if message.role == "user":
      formatted_messages.append(HumanMessage(content=message.content))
    else:
      formatted_messages.append(AIMessage(content=message.content))

  return formatted_messages

def create_system_message(challenge: Challenge) -> SystemMessage:
  return SystemMessage(content=challenge.model_dump_json())