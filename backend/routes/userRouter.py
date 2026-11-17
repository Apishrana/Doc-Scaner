from controllers.authController import getCurrentUser
from fastapi import Depends
from fastapi.routing import APIRouter
from models.user import User

userRouter = APIRouter(prefix="/user", tags=["User"])


@userRouter.get("/me")
def me(user: User = Depends(getCurrentUser)):  # noqa: B008
    return user
