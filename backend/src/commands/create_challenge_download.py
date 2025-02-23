from mediator import MediatorDTO, mediator
from models.entities import Challenge
from database.mongo import engine
import zipfile
from odmantic import ObjectId
from fastapi import HTTPException
from io import BytesIO

class CreateChallengeDownloadCommand(MediatorDTO):
  challenge_id: str

class CreateChallengeDownloadResponse(MediatorDTO):
  file_contents: bytes

@mediator.register_handler(CreateChallengeDownloadCommand)
async def create_challenge_download(command: CreateChallengeDownloadCommand):
  challenge = await engine.find_one(Challenge, Challenge.id == ObjectId(command.challenge_id))
  if challenge is None:
    raise HTTPException(status_code=404)

  buffer = BytesIO()
  with zipfile.ZipFile(buffer, "w") as zip_file:
    for file in challenge.files:
      zip_file.writestr(file.file_name, file.content)

  return CreateChallengeDownloadResponse(file_contents=buffer.getvalue())