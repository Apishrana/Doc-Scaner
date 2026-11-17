from fastapi import UploadFile


async def processDocument(file: UploadFile):
    print(await file.read())
