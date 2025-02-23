import { zodResolver } from "@hookform/resolvers/zod"
import { useNavigate } from "@remix-run/react"
import { useMutation } from "@tanstack/react-query"
import { useState } from "react"
import { useForm } from "react-hook-form"
import { toast } from "sonner"
import * as z from "zod"
import { Button } from "~/components/ui/button"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "~/components/ui/dialog"
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
} from "~/components/ui/form"
import { Input } from "~/components/ui/input"
import { useLocalStorage } from "~/hooks/use-local-storage"
import challengeService from "../challenge-service"
import { Challenge } from "../types"

export interface CompleteChallengeDialogProps {
  challenge: Challenge
  children: React.ReactNode
}

const CompleteChallengeSchema = z.object({
  flag: z.string().min(1),
})

export default ({ children, challenge }: CompleteChallengeDialogProps) => {
  const [open, setOpen] = useState(false)
  const [recentChallenges, setRecentChallenges] = useLocalStorage<Challenge[]>(
    "recent-challenges",
    [],
  )
  const navigate = useNavigate()
  const form = useForm<z.infer<typeof CompleteChallengeSchema>>({
    resolver: zodResolver(CompleteChallengeSchema),
    defaultValues: {
      flag: "",
    },
  })

  const { mutate: completeChallenge, isPending } = useMutation({
    mutationFn: (flag: string) => {
      return challengeService.mutations.completeChallenge(challenge.id, flag)
    },
    onSuccess: () => {
      toast("Flag is correct. Challenge complete!")
      setRecentChallenges(
        recentChallenges.filter((other) => other.id !== challenge.id),
      )
      navigate("/")
    },
    onError: () => {
      toast("Flag is incorrect. Please try again.")
    },
  })

  function onSubmit(data: z.infer<typeof CompleteChallengeSchema>) {
    completeChallenge(data.flag)
  }

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>{children}</DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Complete Challenge</DialogTitle>
        </DialogHeader>
        <DialogDescription>
          <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
            <Form {...form}>
              <FormField
                control={form.control}
                name="flag"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Flag</FormLabel>
                    <FormControl>
                      <Input {...field} />
                    </FormControl>
                  </FormItem>
                )}
              />
              <Button type="submit" disabled={isPending}>
                {isPending ? "Submitting..." : "Submit"}
              </Button>
            </Form>
          </form>
        </DialogDescription>
      </DialogContent>
    </Dialog>
  )
}
