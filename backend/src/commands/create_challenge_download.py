from mediator import MediatorDTO, mediator
from models.entities import Challenge
from database.mongo import engine
import zipfile
from odmantic import ObjectId
from fastapi import HTTPException

class CreateChallengeDownloadCommand(MediatorDTO):
  challenge_id: str

class CreateChallengeDownloadResponse(MediatorDTO):
  file_contents: bytes

@mediator.register_handler(CreateChallengeDownloadCommand)
async def create_challenge_download(command: CreateChallengeDownloadCommand):
  challenge = await engine.find_one(Challenge, Challenge.id == ObjectId(command.challenge_id))
  if challenge is None:
    raise HTTPException(status_code=404)

  zip_file = zipfile.ZipFile("challenge.zip", "w")

  for file in challenge.files:
    zip_file.write(file.path, file.name)

  zip_file.close()

  return CreateChallengeDownloadResponse(file_contents=zip_file.read())