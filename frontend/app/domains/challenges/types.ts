export enum ChallengeCategory {
  WEB_SECURITY = "Web Security",
  CRYPTOGRAPHY = "Cryptography",
  REVERSE_ENGINEERING = "Reverse Engineering",
  FORENSICS = "Forensics",
  BINARY_EXPLOITATION = "Binary Exploitation",
  MISC = "Miscellaneous"
}

export enum ChallengeDifficulty {
  EASY = "Easy",
  MEDIUM = "Medium",
  HARD = "Hard",
  EXPERT = "Expert"
}

export interface Challenge {
  id: string
  category: ChallengeCategory
  difficulty: ChallengeDifficulty
}