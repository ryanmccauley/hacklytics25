from pydantic import BaseModel, ConfigDict
from models.enums import CTFCategory, CTFDifficulty
from pydantic.alias_generators import to_camel

class CreateCTFRequest(BaseModel):
  model_config = ConfigDict(alias_generator=to_camel)

  category: CTFCategory
  difficulty: CTFDifficulty
  additional_prompt: str