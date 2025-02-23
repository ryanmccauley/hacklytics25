from mediator import mediator, MediatorDTO
from models.entities import Challenge
from database.mongo import engine
from odmantic import ObjectId
from typing import Optional


class GetChallengeQuery(MediatorDTO):
    challenge_id: str


class GetChallengeQueryResponse(MediatorDTO):
    challenge: Optional[Challenge]


@mediator.register_handler(GetChallengeQuery)
async def get_challenge(query: GetChallengeQuery):
    challenge = await engine.find_one(
        Challenge, Challenge.id == ObjectId(query.challenge_id)
    )

    return GetChallengeQueryResponse(challenge=challenge)
