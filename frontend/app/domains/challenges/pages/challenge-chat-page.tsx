import { Button } from "~/components/ui/button"
import { Challenge } from "../types"
import { ChevronLeftIcon, CloudDownloadIcon } from "lucide-react"
import { Link } from "@remix-run/react"

export interface ChallengeChatPageProps {
  challenge: Challenge
}

export default ({ challenge }: ChallengeChatPageProps) => {
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