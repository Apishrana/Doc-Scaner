from controllers.authController import loginController, signupController
from db import getSession
from fastapi import Depends
from fastapi.routing import APIRouter
from models.user import LoginModal, SignupModal
from sqlmodel import Session

authRouter = APIRouter(prefix="/auth")


@authRouter.post("/login")
def login(userInput: LoginModal, session: Session = Depends(getSession)):  # noqa: B008
    return loginController(userInput, session)


@authRouter.post("/signup")
def signup(
    userInput: SignupModal, session: Session = Depends(getSession)  # noqa: B008
):
    return signupController(userInput, session)
