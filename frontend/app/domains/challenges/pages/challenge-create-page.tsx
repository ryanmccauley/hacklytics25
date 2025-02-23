import { Button } from "~/components/ui/button"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "~/components/ui/select"
import { Link } from "@remix-run/react"
import { WandSparklesIcon } from "lucide-react"
import { Challenge, ChallengeCategory, ChallengeDifficulty } from "../types"
import { useNavigate } from "@remix-run/react"
import challengeService from "../challenge-service"
import * as z from "zod"
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { useMutation } from "@tanstack/react-query"
import { Form, FormControl, FormField, FormItem, FormLabel } from "~/components/ui/form"
import { Textarea } from "~/components/ui/textarea"
import { useLocalStorage } from "~/hooks/use-local-storage"

const CreateChallengeFormSchema = z.object({
  category: z.nativeEnum(ChallengeCategory),
  difficulty: z.nativeEnum(ChallengeDifficulty),
  additionalPrompt: z.string().optional(),
})

export default function CreateChallengePage() {
  const [recentChallenges, setRecentChallenges] = useLocalStorage<Challenge[]>("recent-challenges", [])
  const navigate = useNavigate()
  const form = useForm<z.infer<typeof CreateChallengeFormSchema>>({
    resolver: zodResolver(CreateChallengeFormSchema),
    defaultValues: {
      category: ChallengeCategory.WebExploitation,
      difficulty: ChallengeDifficulty.EASY,
      additionalPrompt: "",
    },
  })

  function onSubmit(values: z.infer<typeof CreateChallengeFormSchema>) {
    createChallenge(values)
  }

  const {
    mutate: createChallenge,
    isPending
  } = useMutation({
    mutationFn: challengeService.mutations.createChallenge,
    onSuccess: (data) => {
      navigate(`/challenge/${data.id}`)
    }
  })

  return (
    <div className="flex flex-col items-center space-y-8 justify-center min-h-screen p-16">
      <div className="flex flex-col space-y-4 bg-white rounded-lg shadow-sm p-4 w-full max-w-3xl">
        <div className="flex flex-col space-y-2">
          <div className="flex items-center space-x-2">
            <WandSparklesIcon className="bg-red-500 p-2 rounded-lg text-white size-9" />
            <h1 className="text-2xl font-bold">InstantCTF</h1>
          </div>
          <p className="text-gray-800">
            Easy way to create unique CTF-like challenges within seconds. Ask the AI assistant questions about the challenge or type the flag to check if it's correct.
          </p>
        </div>
        <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
          <Form {...form}>
            <FormField
              control={form.control}
              name="category"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Category</FormLabel>
                  <FormControl>
                    <Select
                      onValueChange={field.onChange}
                      defaultValue={field.value}
                    >
                      <FormItem>
                        <SelectTrigger>
                          <SelectValue placeholder="Select a category" />
                        </SelectTrigger>
                      </FormItem>
                      <SelectContent>
                        {Object.values(ChallengeCategory).map((category) => (
                          <SelectItem key={category} value={category}>
                            {category}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </FormControl>
                </FormItem>
              )}
            />
            <FormField
              control={form.control}
              name="difficulty"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Difficulty</FormLabel>
                  <FormControl>
                    <Select
                      onValueChange={field.onChange}
                      defaultValue={field.value}
                    >
                      <FormItem>
                        <SelectTrigger>
                          <SelectValue placeholder="Select a difficulty" />
                        </SelectTrigger>
                      </FormItem>
                      <SelectContent>
                        {Object.values(ChallengeDifficulty).map((difficulty) => (
                          <SelectItem key={difficulty} value={difficulty}>
                            {difficulty}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select> 
                  </FormControl>
                </FormItem>
              )}
            />
            <FormField
              control={form.control}
              name="additionalPrompt"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Additional Prompt</FormLabel>
                  <FormControl>
                    <Textarea
                      placeholder="Enter additional prompt"
                      value={field.value}
                      onChange={field.onChange}
                      className="resize-none"
                    />
                  </FormControl>
                </FormItem>
              )}
            />
            <div className="flex justify-end">
              <Button type="submit" disabled={isPending}>
                {isPending ? "Pending..." : "Create Challenge"}
              </Button>
            </div>
          </Form>
        </form>
      </div>
      <div className="flex flex-col space-y-4 max-w-3xl w-full">
        <h2 className="text-lg font-medium">
          Recent challenges
        </h2>
        <div className="flex flex-col space-y-2">
          {recentChallenges.map((challenge) => (
            <Link
              to={`/challenge/${challenge.id}`} 
              key={challenge.id}
            >
              <Button
                variant="ghost"
                className="w-full justify-start"
              >
                {challenge.title}
              </Button>
            </Link>
          ))}
        </div>
      </div>
    </div>
  )
}