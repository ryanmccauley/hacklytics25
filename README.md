# InstantCTF Product Requirements

## Problem
There are a limited number of practice CTF problems available on the internet. We want to solve this by creating an AI chatbot that would allow users to input details of the type of CTF practice they want to do (e.g. difficulty, category)
and the AI would create a CTF that the user can try.

## User Flow

1. On our web interface, the user initializes the AI by submitting a form with the following fields:
- Category: Web Exploitation, Reverse Engineering, and SQL Injection
- Difficulty: Easy, Medium, or Hard
- Prompt: This is an optional field. The user can specify anything extra that they want the AI to consider when creating their custom CTF.

2. Once the user submits their request, an LLM is given the user's request information and will create an outline that determines the following:
- What kind of challenge within the category should they do?
- What code is needed to achieve this?

3. Once the LLM creates an outline, we will give the outline and the user's context to an LLM to create the output files for the user's CTF. These files are the following:
- Challenge instructions
- Setup instructions

4. Once the output files are created, we will utilize another LLM step to check the files and make sure that everything follows the instructions to send to the computer. If not, we loop the 3rd and 4th steps until complete.

5. Once verified, the user will receive a response with the output information. The user will then be sent to a chat where they can ask for questions, clarifications, hints, and more. Instead of a flag like a normal CTF, the user will have to describe what the solution is. This ensures that the user understands the key challenge.

## Tech Stack
- Frontend: Remix, Tailwind, Shadcn, React Query
- Backend: FastAPI, MongoDb, LangChain
