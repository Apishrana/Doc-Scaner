from fastapi import FastAPI
from routes.authRouter import authRouter

app = FastAPI()

app.add_api_route("/auth", authRouter)

