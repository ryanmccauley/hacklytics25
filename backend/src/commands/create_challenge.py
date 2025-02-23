from mediator import MediatorDTO, mediator
from models.enums import ChallengeCategory, ChallengeDifficulty
from models.entities import Challenge
from database.mongo import engine
from typing import Optional
from langchain_openai import ChatOpenAI
from pydantic import BaseModel
from settings import global_settings
from odmantic import ObjectId
from langchain_core.prompts import PromptTemplate

class CreateChallengeCommand(MediatorDTO):
  category: ChallengeCategory
  difficulty: ChallengeDifficulty
  additional_prompt: Optional[str] = None

class CreateChallengeResponse(MediatorDTO):
  challenge_id: ObjectId

@mediator.register_handler(CreateChallengeCommand)
async def create_challenge(command: CreateChallengeCommand) -> CreateChallengeResponse:
  challenge = Challenge(
    category=command.category,
    difficulty=command.difficulty,
    additional_prompt=command.additional_prompt
  )

  await engine.save(challenge)

  outline = await create_challenge_outline(command)

  print(outline)

  return CreateChallengeResponse(challenge_id=challenge.id)

async def create_challenge_outline(command: CreateChallengeCommand):
  model = ChatOpenAI(model="gpt-4o", api_key=global_settings.OPENAI_API_KEY)
  prompt = PromptTemplate.from_template("""
You are an expert in creating CTF challenges. The user will provide you with a category, difficulty, and an optional additional prompt.
Your goal is to create an outline for another AI Agent to create and implement the challenge.
                                        
Here is the category, difficulty, and additional prompt:

Category: {category}
Difficulty: {difficulty}
Additional Prompt: {additional_prompt}
                                        
Here are some questions to consider:
What kind of challenge within the category should they do?
What code is needed to achieve this?
""")

  response = model.invoke(prompt.format(
    category=command.category.value,
    difficulty=command.difficulty.value,
    additional_prompt=command.additional_prompt
  ))

  return response.content