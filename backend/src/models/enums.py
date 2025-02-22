from enum import Enum

class CTFCategory(Enum):
  WebExploitation = "WebExploitation"
  ReverseEngineering = "ReverseEngineering"
  SQLInjection = "SQLInjection"

class CTFDifficulty(Enum):
  Easy = "Easy"
  Medium = "Medium"
  Hard = "Hard"