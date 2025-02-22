from mediator import MediatorDTO, mediator
from models.enums import ChallengeCategory, ChallengeDifficulty
from models.entities import Challenge
from database.mongo import engine
from typing import Optional

class CreateChallengeCommand(MediatorDTO):
  category: ChallengeCategory
  difficulty: ChallengeDifficulty
  additional_prompt: Optional[str] = None

class CreateChallengeResponse(MediatorDTO):
  challenge_id: str

@mediator.register_handler(CreateChallengeCommand)
async def create_challenge(command: CreateChallengeCommand) -> CreateChallengeResponse:
  challenge = Challenge(
    category=command.category,
    difficulty=command.difficulty,
    additional_prompt=command.additional_prompt
  )

  await engine.save(challenge)

  return CreateChallengeResponse(challenge_id=challenge.id)