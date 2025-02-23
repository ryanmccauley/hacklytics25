import http from "~/lib/axios"
import { Challenge, CreateChallengeRequest } from "./types"
import { Message } from "~/hooks/use-chat-messages";

const BASE_PATH = '/challenges'

export default {
  key: 'challenge',
  mutations: {
    createChallenge: async (request: CreateChallengeRequest) => {
      const { data } = await http.post<Challenge>(`${BASE_PATH}/`, request);
      return data;
    },
    createMessage: async (challengeId: string, message: Omit<Message, "id">) => {
      const { data } = await http.post<Message>(`${BASE_PATH}/${challengeId}/messages`, { ...message })
      return data
    },
    createChatCompletion: async function* (id: string, messages: Message[]) {
      const { data: stream } = await http.post(
        `${BASE_PATH}/${id}/chat-completion`,
        { messages },
        {
          headers: {
            Accept: "text/event-stream",
          },
          responseType: "stream",
          adapter: "fetch",
        },
      )

      const decoder = new TextDecoder("utf-8")
      for await (const chunk of stream as AsyncIterable<Uint8Array>) {
        yield decoder.decode(chunk, { stream: true })
      }
    }
  },
  queries: {
    getChallenge: async (id: string) => {
      const { data } = await http.get<Challenge>(`${BASE_PATH}/${id}`)
    
      return data
    },
    getChallengeFiles: async (id: string) => {
      const { data } = await http.get(`${BASE_PATH}/${id}/files`, {
        responseType: 'blob'
      })

      return data
    },
    listMessages: async (challengeId: string) => {
      const { data } = await http.get<Message[]>(`${BASE_PATH}/${challengeId}/messages`)
      return data
    }
  }
} as const