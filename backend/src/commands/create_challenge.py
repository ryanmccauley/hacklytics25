from mediator import MediatorDTO, mediator
from models.enums import ChallengeCategory, ChallengeDifficulty
from models.entities import Challenge, ChallengeFile
from database.mongo import engine
from typing import Optional
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, ConfigDict, Field
from settings import global_settings
from odmantic import ObjectId
from langchain_core.prompts import PromptTemplate
from prompts import CHALLENGE_OUTLINE_PROMPT, CHALLENGE_INSTRUCTIONS_PROMPT


class CreateChallengeCommand(MediatorDTO):
    category: ChallengeCategory
    difficulty: ChallengeDifficulty
    additional_prompt: Optional[str] = None


class CreateChallengeResponse(MediatorDTO):
    challenge: Challenge


class ChallengeOuptut(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    title: str
    setup_instructions: str = Field(
        description="List of instructions for the user to setup the challenge on their environment. This will be stored in an README.md file"
    )
    description: str = Field(
        description="A short one to two sentence description of the challenge"
    )
    flag_solution: str = Field(description="The solution to the challenge")
    files: list[ChallengeFile]


@mediator.register_handler(CreateChallengeCommand)
async def create_challenge(command: CreateChallengeCommand) -> CreateChallengeResponse:
    outline = await create_challenge_outline(command)
    output = await create_challenge_output(outline)

    challenge = Challenge(
        id=ObjectId(),
        category=command.category,
        difficulty=command.difficulty,
        title=output.title,
        setup_instructions=output.setup_instructions,
        description=output.description,
        flag_solution=output.flag_solution,
        files=output.files,
    )

    await engine.save(challenge)

    return CreateChallengeResponse(challenge=challenge)


async def create_challenge_outline(command: CreateChallengeCommand) -> str:
    model = ChatOpenAI(
        model="o3-mini-2025-01-31",
        api_key=global_settings.OPENAI_API_KEY,
        max_completion_tokens=4096,
    )
    prompt = PromptTemplate.from_template(CHALLENGE_OUTLINE_PROMPT)
    response = model.invoke(
        prompt.invoke(
            {
                "category": command.category.value,
                "difficulty": command.difficulty.value,
                "additional_prompt": command.additional_prompt,
            }
        )
    )

    return response.content


async def create_challenge_output(outline: str) -> ChallengeOuptut:
    model = ChatOpenAI(
        model="o3-mini-2025-01-31",
        api_key=global_settings.OPENAI_API_KEY,
        max_completion_tokens=4096,
    )
    structured_model = model.with_structured_output(ChallengeOuptut)
    prompt = PromptTemplate.from_template(CHALLENGE_INSTRUCTIONS_PROMPT)

    response = structured_model.invoke(prompt.invoke({"outline": outline}))

    return response
