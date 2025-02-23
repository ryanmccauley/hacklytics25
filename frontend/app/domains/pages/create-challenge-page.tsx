import { Button } from "~/components/ui/button"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "~/components/ui/dropdown-menu"
import { useState } from "react"
import { ChevronDown } from "lucide-react"

export default () => {
  const [selectedCategory, setSelectedCategory] = useState("Challenge Category")
  const [selectedDifficulty, setSelectedDifficulty] = useState("Challenge Difficulty")
  return (
    <div className="flex flex-col h-full items-center justify-center">
      <div className="bg-white max-w-4xl w-full rounded-lg shadow-sm border border-gray-200 p-8 flex flex-col space-y-4">
        <div className="flex flex-col">
          <h1
            className="text-2xl font-semibold tracking-tight"
          >
            InstantCTF
          </h1>
          <p>
            Create your own tailored CTF challenges in minutes
          </p>
        </div>
        <div className="flex flex-col space-y-2">
          <div className="flex flex-col">
            <h5>
              Challenge Category
            </h5>
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="outline" className="w-full justify-between">
                  {selectedCategory}
                  <ChevronDown className="h-4 w-4 opacity-50" />
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent className="w-full min-w-[200px]">
                <DropdownMenuItem onClick={() => setSelectedCategory("Web Exploitation")}>
                  Web Exploitation
                </DropdownMenuItem>
                <DropdownMenuItem onClick={() => setSelectedCategory("Reverse Engineering")}>
                  Reverse Engineering
                </DropdownMenuItem>
                <DropdownMenuItem onClick={() => setSelectedCategory("SQL Injection")}>
                  Miscellaneous
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          </div>
          <div className="flex flex-col">
            <h5>
              Challenge Difficulty
            </h5>
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="outline" className="w-full justify-between">
                  {selectedDifficulty}
                  <ChevronDown className="h-4 w-4 opacity-50" />
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent className="w-full min-w-[200px]">
                <DropdownMenuItem onClick={() => setSelectedDifficulty("Easy")}>
                  Easy
                </DropdownMenuItem>
                <DropdownMenuItem onClick={() => setSelectedDifficulty("Medium")}>
                  Medium
                </DropdownMenuItem>
                <DropdownMenuItem onClick={() => setSelectedDifficulty("Hard")}>
                  Hard
                </DropdownMenuItem>
                <DropdownMenuItem onClick={() => setSelectedDifficulty("Impossible")}>
                  Impossible
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>

          </div>
          <div className="flex flex-col">
            <h5>
              Additional Information
            </h5>
          </div>
          <div className="flex items-center justify-end">
            <Button
              size="lg"
            >
              Create Challenge
            </Button>
          </div>
        </div>
      </div>
    </div>
  )
}