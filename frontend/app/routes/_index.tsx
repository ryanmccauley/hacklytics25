import type { MetaFunction } from "@remix-run/node"
import ChallengeCreatePage from "~/domains/challenges/pages/challenge-create-page"

export const meta: MetaFunction = () => {
  return [
    { title: "InstantCTF" },
    {
      name: "description",
      content:
        "Utilize LLMs to generate capture the flag challenges to train prospective software engineers on cybersecurity",
    },
  ]
}

export default () => {
  return <ChallengeCreatePage />
}
