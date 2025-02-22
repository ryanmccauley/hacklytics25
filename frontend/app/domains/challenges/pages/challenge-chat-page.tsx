import { Challenge } from "../types"

export interface ChallengeChatPageProps {
  challenge: Challenge
}

export default ({ challenge }: ChallengeChatPageProps) => {
  return (
    <p>Challenge</p>
  )
}