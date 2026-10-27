from fastapi.routing import APIRouter

authRouter = APIRouter()


@authRouter.get("/login")
def login():
    pass
