from enum import Enum


class ChallengeCategory(Enum):
    WebExploitation = "WebExploitation"
    ReverseEngineering = "ReverseEngineering"
    SQLInjection = "SQLInjection"


class ChallengeDifficulty(Enum):
    Easy = "Easy"
    Medium = "Medium"
    Hard = "Hard"
