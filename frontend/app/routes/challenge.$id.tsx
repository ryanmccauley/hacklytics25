import { useLoaderData } from "@remix-run/react"
import challengeService from "~/domains/challenges/challenge-service"
import ChallengeChatPage from "~/domains/pages/challenge-chat-page"

export async function clientLoader({ params: { id } }: { params: { id: string } }) {
  const challenge = await challengeService.queries.getChallenge(id)

  return challenge
}

export default () => {
  const challenge = useLoaderData<typeof clientLoader>()

  return (
    <ChallengeChatPage challenge={challenge} />
  )
}