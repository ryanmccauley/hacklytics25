import { Link } from "@remix-run/react"
import { useMutation } from "@tanstack/react-query"
import {
  BookOpenIcon,
  ChevronLeftIcon,
  CloudDownloadIcon,
  FlagIcon,
  FlipHorizontal2,
} from "lucide-react"
import { useEffect, useMemo, useReducer, useState } from "react"
import ReactMarkdown from "react-markdown"
import { Badge } from "~/components/ui/badge"
import { Button } from "~/components/ui/button"
import { Message, useChatMessages } from "~/hooks/use-chat-messages"
import { useLocalStorage } from "~/hooks/use-local-storage"
import { cn } from "~/lib/utils"
import challengeService from "../challenge-service"
import ChatTextInput from "../components/chat-text-input"
import CompleteChallengeDialog from "../components/complete-challenge-dialog"
import ViewInstructionsDialog from "../components/view-instructions-dialog"
import { Challenge, ChallengeDifficulty } from "../types"
import { toast } from "sonner"

export interface ChallengeChatPageProps {
  challenge: Challenge
  messages: Message[]
}

export default ({
  challenge,
  messages: initialMessages,
}: ChallengeChatPageProps) => {
  const [content, setContent] = useState("")
  const [viewInstructionsDialogOpen, setViewInstructionsDialogOpen] =
    useState(true)
  const [recentChallenges, setRecentChallenges] = useLocalStorage<Challenge[]>(
    "recent-challenges",
    [],
  )
  const [messages, dispatch] = useReducer(useChatMessages, initialMessages)

  useEffect(() => {
    if (!recentChallenges.some((other) => other.id === challenge.id)) {
      setRecentChallenges([...recentChallenges, challenge])
    }
  }, [])

  async function downloadChallengeFiles() {
    const files = await challengeService.queries.getChallengeFiles(challenge.id)
    const url = window.URL.createObjectURL(new Blob([files]))
    const a = document.createElement("a")
    a.href = url
    a.download = `challenge-${challenge.id}.zip`
    document.body.appendChild(a)
    a.click()
    a.remove()

    toast("Challenge files downloaded successfully")
  }

  async function onSubmit() {
    if (isLoading) return
    if (content.trim().length != 0) {
      await createMessage(content)
    }

    await createChatCompletion()
  }

  const { mutateAsync: createMessage, isPending: isCreatingMessage } =
    useMutation({
      mutationFn: (content: string) => {
        return challengeService.mutations.createMessage(challenge.id, {
          content,
          role: "user",
        })
      },
      onMutate: async (message) => {
        const previousContent = content
        const previousMessages = messages
        const optimisticMessage = {
          id: crypto.randomUUID(),
          content: previousContent,
          role: "user",
        } as Message

        setContent("")

        dispatch({
          type: "add",
          message: optimisticMessage,
        })

        return {
          previousContent,
          previousMessages,
          optimisticMessage,
        }
      },
      onError: (error, message, context) => {
        dispatch({
          type: "pop",
        })

        if (context !== undefined) {
          setContent(context.previousContent)
          dispatch({
            type: "set",
            messages: context.previousMessages,
          })
        }
      },
      onSuccess: (data, message, context) => {
        dispatch({
          type: "update",
          id: context.optimisticMessage.id,
          message: data,
        })
      },
    })

  const {
    mutateAsync: createChatCompletion,
    isPending: isCreatingChatCompletion,
  } = useMutation({
    mutationFn: async () => {
      const optimisticMessage = {
        id: crypto.randomUUID(),
        content: "",
        role: "assistant",
      } as Message

      dispatch({
        type: "add",
        message: optimisticMessage,
      })

      const response = challengeService.mutations.createChatCompletion(
        challenge.id,
        messages,
      )

      for await (const chunk of response) {
        optimisticMessage.content += chunk

        dispatch({
          type: "update",
          id: optimisticMessage.id,
          message: optimisticMessage,
        })
      }

      return optimisticMessage
    },
    // onMutate: async (message) => {
    //   const previousContent = content
    //   const previousMessages = messages

    //   const optimisticUserMessage = {
    //     id: crypto.randomUUID(),
    //     content: previousContent,
    //     role: "user"
    //   } as Message

    //   dispatch({
    //     type: "add",
    //     message: optimisticUserMessage
    //   })

    //   setContent("")

    //   return {
    //     previousContent,
    //     previousMessages,
    //     optimisticUserMessage
    //   }
    // },
    onError: (error, messages, context) => {
      // if (context !== undefined) {
      //   setContent(context.previousContent)
      //   dispatch({
      //     type: "set",
      //     messages: context.previousMessages
      //   })
      // }
    },
    onSuccess: (data, message, context) => {
      // if (context !== undefined) {
      //   dispatch({
      //     type: "update",
      //     id: context.optimisticUserMessage.id,
      //     message: data
      //   })
      // }
    },
  })

  const isLoading = useMemo(() => {
    return isCreatingMessage || isCreatingChatCompletion
  }, [isCreatingMessage, isCreatingChatCompletion])

  return (
    <div className="min-h-screen max-h-screen flex flex-col items-center">
      <div className="w-full p-4 flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <Link to="/">
            <Button variant="ghost" size="icon">
              <ChevronLeftIcon className="scale-140" />
            </Button>
          </Link>
          <div className="flex items-center space-x-2">
            <h2 className="text-lg font-medium">{challenge.title}</h2>
            <Badge
              variant="outline"
              className={cn(
                "text-sm",
                challenge.difficulty === ChallengeDifficulty.EASY &&
                  "bg-green-500/20",
                challenge.difficulty === ChallengeDifficulty.MEDIUM &&
                  "bg-yellow-500/20",
                challenge.difficulty === ChallengeDifficulty.HARD &&
                  "bg-red-500/20",
              )}
            >
              {challenge.difficulty}
            </Badge>
          </div>
        </div>
        <div className="flex items-center space-x-2">
          <CompleteChallengeDialog challenge={challenge}>
            <Button variant="outline" size="lg">
              <FlagIcon />
              Complete Challenge
            </Button>
          </CompleteChallengeDialog>
          <ViewInstructionsDialog
            open={viewInstructionsDialogOpen}
            onOpenChange={setViewInstructionsDialogOpen}
            instructions={challenge.setup_instructions}
          >
            <Button variant="outline" size="lg">
              <BookOpenIcon />
              View Instructions
            </Button>
          </ViewInstructionsDialog>
          <Button variant="outline" size="lg" onClick={downloadChallengeFiles}>
            <CloudDownloadIcon />
            Download Files
          </Button>
        </div>
      </div>
      <div className="flex-1 overflow-y-scroll no-scrollbar max-w-3xl w-full space-y-2">
        {messages.map((message) => (
          <ChatMessage key={message.id} message={message} />
        ))}
      </div>
      <ChatTextInput
        disabled={isLoading}
        value={content}
        onChange={setContent}
        onSubmit={onSubmit}
      />
    </div>
  )
}

function ChatMessage({ message }: { message: Message }) {
  return (
    <div
      className={cn(
        message.role === "user" ? "justify-end" : "justify-start",
        "flex items-center",
      )}
    >
      <div
        className={cn(
          message.role === "user" && "bg-gray-200 rounded-lg",
          "p-2 prose",
        )}
      >
        <ReactMarkdown>{message.content}</ReactMarkdown>
      </div>
    </div>
  )
}
