import { Button } from "~/components/ui/button"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "~/components/ui/dropdown-menu"
import { useState } from "react"
import { ChevronDown } from "lucide-react"
import { ChallengeCategory, ChallengeDifficulty } from "../types"
import { useNavigate } from "@remix-run/react"
import challengeService from "../challenge-service"

export default function CreateChallengePage() {
  const [selectedCategory, setSelectedCategory] = useState<ChallengeCategory>(ChallengeCategory.WebExploitation)
  const [selectedDifficulty, setSelectedDifficulty] = useState<ChallengeDifficulty>(ChallengeDifficulty.EASY)
  const [additionalPrompt, setAdditionalPrompt] = useState("")
  const navigate = useNavigate()

  async function onSubmit(event: React.FormEvent) {
    event.preventDefault()
    try {
      const response = await challengeService.mutations.createChallenge({
        category: selectedCategory,
        difficulty: selectedDifficulty,
        additionalPrompt,
      });
      navigate(`/challenge/${response.id}`);
    } catch (error) {
      console.error("Error creating challenge:", error);
      // Handle the error, show a message to the user
    }
  }

  return (
    <div className="flex flex-col h-full items-center justify-center">
      <div className="bg-white max-w-4xl w-full rounded-lg shadow-sm border border-gray-200 p-8 flex flex-col space-y-4">
        <div className="flex flex-col">
          <h1 className="text-2xl font-semibold tracking-tight">
            InstantCTF
          </h1>
          <p>
            Create your own tailored CTF challenges in minutes
          </p>
        </div>
        <form onSubmit={onSubmit} className="flex flex-col space-y-2">
          <div className="flex flex-col">
            <label htmlFor="category" className="block text-sm font-medium text-gray-700">
              Challenge Category
            </label>
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="outline" className="w-full justify-between">
                  {selectedCategory}
                  <ChevronDown className="h-4 w-4 opacity-50" />
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent className="w-full min-w-[200px]">
                {Object.values(ChallengeCategory).map((category) => (
                  <DropdownMenuItem
                    key={category}
                    onClick={() => setSelectedCategory(category)}
                  >
                    {category}
                  </DropdownMenuItem>
                ))}
              </DropdownMenuContent>
            </DropdownMenu>
          </div>

          <div className="flex flex-col">
            <label htmlFor="difficulty" className="block text-sm font-medium text-gray-700">
              Difficulty Level
            </label>
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="outline" className="w-full justify-between">
                  {selectedDifficulty}
                  <ChevronDown className="h-4 w-4 opacity-50" />
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent className="w-full min-w-[200px]">
                {Object.values(ChallengeDifficulty).map((difficulty) => (
                  <DropdownMenuItem
                    key={difficulty}
                    onClick={() => setSelectedDifficulty(difficulty)}
                  >
                    {difficulty}
                  </DropdownMenuItem>
                ))}
              </DropdownMenuContent>
            </DropdownMenu>
          </div>
          <div className="flex flex-col">
            <label htmlFor="additionalInfo" className="block text-sm font-medium text-gray-700">
              Additional Information
            </label>
            <textarea
              id="additionalInfo"
              name="additionalInfo"
              rows={3}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
              placeholder="Add any specific requirements or context for your challenge"
              value={additionalPrompt}
              onChange={(e) => setAdditionalPrompt(e.target.value)}
            />
          </div>
          <div className="flex items-center justify-end">
            <Button type="submit" size="lg">
              Create Challenge
            </Button>
          </div>
        </form>
      </div>
    </div>
  )
}