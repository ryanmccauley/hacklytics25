from odmantic import Model
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

class ChallengeFile(BaseModel):
  file_name: str
  content: str

class Challenge(Model):
  title: str
  category: str
  difficulty: str
  setup_instructions: str
  description: str
  flag_solution: str
  files: List[ChallengeFile]
  completed_at: Optional[datetime] = None

  @property
  def is_completed(self) -> bool:
    return self.completed_at is not None

  model_config = {
    "collection": "challenges"
  }