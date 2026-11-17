import os

from dotenv import load_dotenv
from fastapi import FastAPI, status
from fastapi.responses import RedirectResponse
from routes.authRouter import authRouter
from routes.fileRouter import fileRouter
from routes.userRouter import userRouter
from uvicorn import run

app = FastAPI(openapi_url="/openapi.json" if os.environ.get("DEBUG") == "True" else "")

app.include_router(authRouter)
app.include_router(userRouter)
app.include_router(fileRouter)


@app.get("/")
def root():
    return RedirectResponse(url="/docs", status_code=status.HTTP_307_TEMPORARY_REDIRECT)


if __name__ == "__main__":
    load_dotenv()
    run(
        "main:app",
        host=os.environ.get("BACKEND_HOST"),
        port=int(os.environ.get("BACKEND_PORT")),
        reload=True,
    )
