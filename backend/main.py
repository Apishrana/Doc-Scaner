import os

from dotenv import load_dotenv
from fastapi import FastAPI
from routes.authRouter import authRouter
from routes.userRouter import userRouter
from uvicorn import run

app = FastAPI(openapi_url="/openapi.json" if os.environ.get("DEBUG") == "True" else "")

app.include_router(authRouter)
app.include_router(userRouter)

if __name__ == "__main__":
    load_dotenv()
    run(
        "main:app",
        host=os.environ.get("BACKEND_HOST"),
        port=int(os.environ.get("BACKEND_PORT")),
        reload=True,
    )
