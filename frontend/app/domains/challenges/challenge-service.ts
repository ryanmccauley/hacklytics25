import http from "~/lib/axios"
import { Challenge } from "../types"

const BASE_PATH = '/challenges'

export default {
  key: 'challenge',
  mutations: {},
  queries: {
    getChallenge: async (id: string) => {
      const { data } = await http.get<Challenge>(`${BASE_PATH}/${id}`)
    
      return data
    }
  }
} as const