import re

from controllers.authController import getCurrentUser
from fastapi import Depends, UploadFile
from fastapi.routing import APIRouter
from models.user import User
from tool.db import supabase
from tool.encryption import encryptFile

fileRouter = APIRouter(prefix="/files")


@fileRouter.post("/upload")
async def upload(file: UploadFile, user: User = Depends(getCurrentUser)):  # noqa: B008
    contents = await file.read()
    res = supabase.storage.from_("scan files").upload(
        path=f"{user.id}/{re.sub(r"[^a-zA-Z0-9._-]", "_", file.filename)}/enc",
        file=encryptFile(contents),
        file_options={
            "content-type": file.content_type,
        },
    )
    return res
