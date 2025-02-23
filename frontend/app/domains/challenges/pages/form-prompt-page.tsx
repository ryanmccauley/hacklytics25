"use client"

import { Button } from "~/components/ui/button";
import { ChallengeCategory, ChallengeDifficulty } from "../types";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "~/components/ui/form";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "~/components/ui/select";
import { Textarea } from "~/components/ui/textarea";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import * as z from "zod";
import { useNavigate, useLoaderData } from "@remix-run/react";
import { Challenge } from "../types";
import challengeService from "../challenge-service";

const formSchema = z.object({
  category: z.nativeEnum(ChallengeCategory),
  difficulty: z.nativeEnum(ChallengeDifficulty),
  additionalPrompt: z.string().optional(),
});

export async function clientLoader({ params: { id } }: { params: { id: string } }) {
  const challenge = await challengeService.queries.getChallenge(id);
  return challenge;
}

export default function FormPromptPage() {
  const navigate = useNavigate();
  const challenge = useLoaderData<typeof clientLoader>();
  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      additionalPrompt: "",
    },
  });

  async function onSubmit(values: z.infer<typeof formSchema>) {
    // Here you'll implement the API call to create the challenge
    console.log(values);
    // After successful creation, navigate to the challenge page
    // navigate(`/challenge/${challengeId}`);
  }

  return (
    <div className="flex flex-col h-full items-center justify-center">
      <div className="bg-white max-w-4xl w-full rounded-lg shadow-sm border border-gray-200 p-8">
        <div className="mb-6">
          <h1 className="text-2xl font-semibold tracking-tight">Challenge: {challenge.name}</h1>
          <p className="text-muted-foreground">{challenge.description}</p>
        </div>

        <div className="mb-6">
          <h2 className="text-xl font-semibold tracking-tight mb-2">Files</h2>
          {/* Here you'll list the challenge files for download */}
        </div>

        <div className="mb-6">
          <h2 className="text-xl font-semibold tracking-tight mb-2">Hints</h2>
          <Textarea placeholder="Ask for a hint" />
          <div className="mt-2">
            <Button>Ask for Hint</Button>
          </div>
        </div>

        <div>
          <h2 className="text-xl font-semibold tracking-tight mb-2">Solution</h2>
          <Textarea placeholder="Describe your solution" />
          <div className="mt-2">
            <Button>Submit Solution</Button>
          </div>
        </div>
      </div>
    </div>
  );
} 