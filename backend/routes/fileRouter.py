from controllers.authController import getCurrentUser
from controllers.fileController import uploadController
from fastapi import Depends, UploadFile
from fastapi.routing import APIRouter
from models.user import User
from sqlmodel import Session
from tool.db import getSession

fileRouter = APIRouter(prefix="/files", tags=["Files"])


@fileRouter.post("/upload")
async def upload(
    file: UploadFile,
    user: User = Depends(getCurrentUser),  # noqa: B008
    session: Session = Depends(getSession),  # noqa: B008
):
    return await uploadController(file, user, session)
