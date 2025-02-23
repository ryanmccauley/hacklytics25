export enum ChallengeCategory {
  WebExploitation = 'WebExploitation',
  ReverseEngineering = 'ReverseEngineering',
  SQLInjection = 'SQLInjection'
}

export enum ChallengeDifficulty {
  EASY = 'Easy',
  MEDIUM = 'Medium',
  HARD = 'Hard',
  EXPERT = 'Expert'
}

export interface Challenge {
  id: string;
  name: string;
  description: string;
  category: ChallengeCategory;
  difficulty: ChallengeDifficulty;
}

export interface CreateChallengeRequest {
  category: ChallengeCategory;
  difficulty: ChallengeDifficulty;
  additionalPrompt?: string;
}