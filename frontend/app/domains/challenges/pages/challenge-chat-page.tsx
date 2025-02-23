import { Button } from "~/components/ui/button"
import { Challenge, ChallengeDifficulty } from "../types"
import { BookOpenIcon, ChevronLeftIcon, CloudDownloadIcon, FlipHorizontal2 } from "lucide-react"
import { Link } from "@remix-run/react"
import challengeService from "../challenge-service"
import { useState } from "react"
import ChatTextInput from "../components/chat-text-input"
import { Badge } from "~/components/ui/badge"
import { cn } from "~/lib/utils"
import ViewInstructionsDialog from "../components/view-instructions-dialog"

export interface ChallengeChatPageProps {
  challenge: Challenge
}

export default ({ challenge }: ChallengeChatPageProps) => {
  const [content, setContent] = useState("")
  const [viewInstructionsDialogOpen, setViewInstructionsDialogOpen] = useState(true)

  async function downloadChallengeFiles() {
    const files = await challengeService.queries.getChallengeFiles(challenge.id)
    const url = window.URL.createObjectURL(new Blob([files]))
    const a = document.createElement('a')
    a.href = url
    a.download = `challenge-${challenge.id}.zip`
    document.body.appendChild(a)
    a.click()
    a.remove()
  }


  return (
    <div className="min-h-screen flex flex-col items-center relative">
      <div className="absolute top-0 left-0 w-full p-4 flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <Link
            to="/"
          >
            <Button
              variant="ghost"
              size="icon"
            >
              <ChevronLeftIcon className="scale-140" />
            </Button>
          </Link>
          <div className="flex items-center space-x-2">
            <h2
              className="text-lg font-medium"
            >
              { challenge.title }
            </h2>
            <Badge
              variant="outline"
              className={cn(
                "text-sm",
                challenge.difficulty === ChallengeDifficulty.EASY && "bg-green-500/20",
                challenge.difficulty === ChallengeDifficulty.MEDIUM && "bg-yellow-500/20",
                challenge.difficulty === ChallengeDifficulty.HARD && "bg-red-500/20",
              )}
            >
              { challenge.difficulty }
            </Badge>
          </div>
        </div>
        <div className="flex items-center space-x-2">
          <ViewInstructionsDialog
            open={viewInstructionsDialogOpen}
            onOpenChange={setViewInstructionsDialogOpen}
            instructions="hello world"
          >
            <Button
              variant="outline"
              size="lg"
            >
              <BookOpenIcon />
              View Instructions
            </Button>
          </ViewInstructionsDialog>
          <Button
            variant="outline"
            size="lg"
            onClick={downloadChallengeFiles}
          >
            <CloudDownloadIcon />
            Download Files
          </Button>
        </div>
      </div>
      <div className="flex-1">

      </div>
      <ChatTextInput
        value={content}
        onChange={setContent}
        onSubmit={() => alert("hello orld")}
      />
    </div>
  )
}