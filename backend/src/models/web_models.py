from pydantic import BaseModel, ConfigDict
from models.enums import ChallengeCategory, ChallengeDifficulty
from pydantic.alias_generators import to_camel
from typing import Optional, List, Literal


class CreateChallengeRequest(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)

    category: ChallengeCategory
    difficulty: ChallengeDifficulty
    additional_prompt: Optional[str] = None


class ChatMessageRequest(BaseModel):
    id: str
    content: str
    role: Literal["user", "assistant"]


class CreateChatCompletionRequest(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    messages: List[ChatMessageRequest]


class CreateMessageRequest(BaseModel):
    content: str
    role: Literal["user", "assistant"]


class CompleteChallengeRequest(BaseModel):
    flag: str
