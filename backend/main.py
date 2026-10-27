import os

from fastapi import FastAPI
from routes.authRouter import authRouter
from uvicorn import run

app = FastAPI(openapi_url="/openapi.json" if os.environ.get("DEBUG") == "True" else "")

app.add_api_route("/auth", authRouter)

if __name__ == "__main__":
    run(
        "main:app",
        host=os.environ.get("BACKEND_HOST"),
        port=os.environ.get("BACKEND_PORT")
    )
