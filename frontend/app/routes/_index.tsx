import type { MetaFunction } from "@remix-run/node"
import ChallengeCreatePage from "~/domains/challenges/pages/challenge-create-page"

export const meta: MetaFunction = () => {
  return [
    { title: "New Remix App" },
    { name: "description", content: "Welcome to Remix!" },
  ]
}

export default () => {
  return <ChallengeCreatePage />
}
