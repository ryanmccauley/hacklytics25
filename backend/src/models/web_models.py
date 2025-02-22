from pydantic import BaseModel, ConfigDict
from models.enums import ChallengeCategory, ChallengeDifficulty
from pydantic.alias_generators import to_camel
from typing import Optional

class CreateChallengeRequest(BaseModel):
  model_config = ConfigDict(alias_generator=to_camel)

  category: ChallengeCategory
  difficulty: ChallengeDifficulty
  additional_prompt: Optional[str] = None