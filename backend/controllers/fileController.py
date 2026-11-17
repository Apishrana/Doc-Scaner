import re
from hashlib import sha256

from fastapi import UploadFile
from models.scans import Documents
from models.user import User
from sqlmodel import Session
from tool.db import supabase
from tool.encryption import encryptFile
from tool.processDocuments import processDocument


async def uploadController(file: UploadFile, user: User, session: Session):
    fileContent = encryptFile(await file.read())
    sha = sha256(fileContent).hexdigest()
    fileName = re.sub(r"[^a-zA-Z0-9._-]", "_", file.filename)
    res = supabase.storage.from_("scan files").upload(
        path=f"{user.id}/{fileName}/enc",
        file=fileContent,
        file_options={
            "content-type": file.content_type,
        },
    )
    doc = Documents(
        user_id=user.id,
        filename=fileName,
        mime_type=file.content_type,
        size_bytes=len(fileContent),
        sha256=sha,
        storage_key=f"{user.id}/{fileName}/enc",
    )
    session.add(doc)
    session.commit()
    session.refresh(doc)
    processDocument(file)
    return res
