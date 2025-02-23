import { Button } from "~/components/ui/button"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "~/components/ui/select"
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
            <Select onValueChange={(value) => console.log(value)}>
        <SelectTrigger className="w-full">
          <SelectValue placeholder="Select a category" />
        </SelectTrigger>
        <SelectContent>
          <SelectItem value="web">Web Exploitation</SelectItem>
          <SelectItem value="reverse">Reverse Engineering</SelectItem>
          <SelectItem value="sql">SQL Injection</SelectItem>
        </SelectContent>
      </Select>
          </div>
          <div className="flex flex-col">
            <h5>
              Challenge Difficulty
            </h5>
            <Select onValueChange={(value) => console.log(value)}>
        <SelectTrigger className="w-full">
          <SelectValue placeholder="Select a category" />
        </SelectTrigger>
        <SelectContent>
          <SelectItem value="Easy">Easy</SelectItem>
          <SelectItem value="Medium">Medium</SelectItem>
          <SelectItem value="Hard">Hard</SelectItem>
          <SelectItem value="Impossible">Impossible</SelectItem>
        </SelectContent>
      </Select>

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