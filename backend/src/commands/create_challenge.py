from mediator import MediatorDTO, mediator
from models.enums import ChallengeCategory, ChallengeDifficulty
from typing import Optional

class CreateChallengeCommand(MediatorDTO):
  category: ChallengeCategory
  difficulty: ChallengeDifficulty
  additional_prompt: Optional[str] = None

class CreateChallengeResponse(MediatorDTO):
  challenge_id: str

@mediator.register_handler(CreateChallengeCommand)
async def create_challenge(command: CreateChallengeCommand) -> CreateChallengeResponse:
  pass