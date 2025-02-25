from fastapi import APIRouter, HTTPException, Depends, Response
from fastapi.responses import StreamingResponse
from database.mongo import engine
from models.entities import Challenge
from models.web_models import CreateChallengeRequest, CreateChatCompletionRequest
from commands.create_challenge import CreateChallengeCommand, CreateChallengeResponse
from mediator import Mediator, get_mediator
from odmantic import ObjectId
from queries.get_challenge import GetChallengeQuery, GetChallengeQueryResponse
from commands.create_challenge_download import (
    CreateChallengeDownloadCommand,
    CreateChallengeDownloadResponse,
)
from commands.create_chat_completion import CreateChallengeChatCompletionCommand
from commands.create_message import CreateMessageCommand, CreateMessageCommandResponse
from io import BytesIO
from queries.list_messages import ListMessagesQuery, ListMessagesQueryResponse
from models.web_models import CreateMessageRequest, CompleteChallengeRequest
from commands.complete_challenge import CompleteChallengeCommand

challenges_router = APIRouter(prefix="/challenges")


@challenges_router.get("/{id}")
async def get_challenge(
    id: str,
    mediator: Mediator[GetChallengeQuery, GetChallengeQueryResponse] = Depends(
        get_mediator
    ),
):
    query = GetChallengeQuery(challenge_id=id)
    response = await mediator.send(query)

    if response.challenge is None:
        raise HTTPException(status_code=404)

    return response.challenge


@challenges_router.post("/")
async def create_challenge(
    request: CreateChallengeRequest,
    mediator: Mediator[CreateChallengeCommand, CreateChallengeResponse] = Depends(
        get_mediator
    ),
):
    command = CreateChallengeCommand(
        category=request.category,
        difficulty=request.difficulty,
        additional_prompt=request.additional_prompt,
    )

    response = await mediator.send(command)

    return response.challenge


@challenges_router.post("/{id}/complete")
async def complete_challenge(
    id: str,
    request: CompleteChallengeRequest,
    mediator: Mediator[CompleteChallengeCommand, any] = Depends(get_mediator),
):
    command = CompleteChallengeCommand(challenge_id=id, flag=request.flag)

    await mediator.send(command)

    return Response(status_code=204)


@challenges_router.get("/{id}/files")
async def create_challenge_download(
    id: str,
    mediator: Mediator[
        CreateChallengeDownloadCommand, CreateChallengeDownloadResponse
    ] = Depends(get_mediator),
):
    command = CreateChallengeDownloadCommand(challenge_id=id)
    response = await mediator.send(command)

    headers = {"Content-Disposition": f"attachment; filename=challenge-{id}.zip"}
    return StreamingResponse(
        BytesIO(response.file_contents), media_type="application/zip", headers=headers
    )


@challenges_router.get("/{id}/messages")
async def list_messages(
    id: str,
    mediator: Mediator[ListMessagesQuery, ListMessagesQueryResponse] = Depends(
        get_mediator
    ),
):
    query = ListMessagesQuery(challenge_id=id)
    response = await mediator.send(query)

    return response.messages


@challenges_router.post("/{id}/messages")
async def create_message(
    id: str,
    request: CreateMessageRequest,
    mediator: Mediator[CreateMessageCommand, CreateMessageCommandResponse] = Depends(
        get_mediator
    ),
):
    command = CreateMessageCommand(
        challenge_id=id, content=request.content, role=request.role
    )

    response = await mediator.send(command)

    return response.message


@challenges_router.post("/{id}/chat-completion")
async def create_challenge_chat_completion(
    id: str,
    request: CreateChatCompletionRequest,
    mediator: Mediator[
        CreateChallengeChatCompletionCommand, StreamingResponse
    ] = Depends(get_mediator),
):
    challenge = await engine.find_one(Challenge, Challenge.id == ObjectId(id))

    if challenge is None:
        raise HTTPException(status_code=404)

    command = CreateChallengeChatCompletionCommand(
        challenge_id=id, messages=request.messages
    )

    response = await mediator.send(command)

    return response
