from odmantic import Model
from datetime import datetime
from typing import Optional

class CTFChallenge(Model):
  category: str
  difficulty: str
  completed_at: Optional[datetime] = None

  @property
  def is_completed(self) -> bool:
    return self.completed_at is not None