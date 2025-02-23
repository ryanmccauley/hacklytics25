import http from "~/lib/axios"
import { Challenge, CreateChallengeRequest } from "../types"

const BASE_PATH = '/challenges'

export default {
  key: 'challenge',
  mutations: {
    createChallenge: async (request: CreateChallengeRequest) => {
      const { data } = await http.post<{ id: string }>(`${BASE_PATH}/`, request);
      return data;
    },
  },
  queries: {
    getChallenge: async (id: string) => {
      const { data } = await http.get<Challenge>(`${BASE_PATH}/${id}`)
    
      return data
    }
  }
} as const