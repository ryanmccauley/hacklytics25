import { useLocalStorage } from "./use-local-storage"

export interface Message {
  id: string
  content: string
  role: "user" | "assistant"
}

type MessageAction =
  | { type: "add"; message: Message }
  | { type: "update"; id: string; message: Message }
  | { type: "set"; messages: Message[] }
  | { type: "delete"; id: string }
  | { type: "pop" }

export function useChatMessages(
  state: Message[],
  action: MessageAction
) {
  switch (action.type) {
    case "add":
      return [...state, action.message]
    case "update":
      return state.map((message) => message.id === action.id ? action.message : message)
    case "set":
      return action.messages
    case "delete":
      return state.filter((message) => message.id !== action.id)
    case "pop":
      return state.slice(0, -1)
  }
}
