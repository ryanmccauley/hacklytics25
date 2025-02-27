from odmantic import Model, ObjectId
from datetime import datetime
from typing import Optional, List, Literal
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

    model_config = {"collection": "challenges"}


class ChatMessage(Model):
    challenge_id: ObjectId
    content: str
    role: Literal["user", "assistant"]
    created_at: datetime

    model_config = {"collection": "chat_messages"}
