export enum ChallengeCategory {
  WebExploitation = "WebExploitation",
  ReverseEngineering = "ReverseEngineering",
  SQLInjection = "SQLInjection",
}

export enum ChallengeDifficulty {
  EASY = "Easy",
  MEDIUM = "Medium",
  HARD = "Hard",
}

export interface ChallengeFile {
  file_name: string
  content: string
}

export interface Challenge {
  id: string
  title: string
  category: ChallengeCategory
  difficulty: ChallengeDifficulty
  setup_instructions: string
  description: string
  flag_solution: string
  files: ChallengeFile[]
}

export interface CreateChallengeRequest {
  category: ChallengeCategory
  difficulty: ChallengeDifficulty
  additional_prompt?: string
}
