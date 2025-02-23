export enum ChallengeCategory {
  WebExploitation = 'WebExploitation',
  ReverseEngineering = 'ReverseEngineering',
  SQLInjection = 'SQLInjection'
}

export enum ChallengeDifficulty {
  EASY = 'Easy',
  MEDIUM = 'Medium',
  HARD = 'Hard'
}

export interface Challenge {
  id: string
  title: string
  category: ChallengeCategory
  difficulty: ChallengeDifficulty
}

export interface CreateChallengeRequest {
  category: ChallengeCategory
  difficulty: ChallengeDifficulty
  additionalPrompt?: string
}