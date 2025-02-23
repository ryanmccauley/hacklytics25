import { Button } from "~/components/ui/button"
import { Challenge } from "../types"
import { ChevronLeftIcon, CloudDownloadIcon } from "lucide-react"
import { Link } from "@remix-run/react"
import challengeService from "../challenge-service"

export interface ChallengeChatPageProps {
  challenge: Challenge
}

export default ({ challenge }: ChallengeChatPageProps) => {
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
    <div className="min-h-screen flex flex-col relative">
      <div className="absolute top-0 left-0 w-full p-4 flex items-center justify-between">
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
        <Button
          variant="outline"
          size="lg"
          onClick={downloadChallengeFiles}
        >
          <CloudDownloadIcon />
          Download Files
        </Button>
      </div>
      <div className="flex-1">

      </div>
      <div className="bg-blue-500 w-full pb-4">
        Hello world
      </div>
    </div>
  )
}