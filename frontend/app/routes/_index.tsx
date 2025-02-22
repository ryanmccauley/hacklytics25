import type { MetaFunction } from "@remix-run/node";
import CreateChallengePage from "~/domains/pages/create-challenge-page";

export const meta: MetaFunction = () => {
  return [
    { title: "New Remix App" },
    { name: "description", content: "Welcome to Remix!" },
  ];
};

export default () => {
  return <CreateChallengePage />
}