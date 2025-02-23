import { useLoaderData } from "@remix-run/react"
import challengeService from "~/domains/challenges/challenge-service"
import ChallengeChatPage from "~/domains/challenges/pages/challenge-chat-page"

export async function clientLoader({ params: { id } }: { params: { id: string } }) {
  const [challenge, messages] = await Promise.all([
    challengeService.queries.getChallenge(id),
    challengeService.queries.listMessages(id)
  ])

  return {
    challenge,
    messages
  }
}

export default () => {
  const { challenge, messages } = useLoaderData<typeof clientLoader>()

  return (
    <ChallengeChatPage challenge={challenge} messages={messages} />
  )
}