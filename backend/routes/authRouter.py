from controllers.authController import authenticateUser, hashPass
from db import supabase
from fastapi.routing import APIRouter
from models.user import LoginModal, SignupModal

authRouter = APIRouter(prefix="/auth")


@authRouter.post("/login")
def login(userInput: LoginModal):
    authenticateUser(userInput.Email, userInput.Password)
    return {"m": 1}


@authRouter.post("/signup")
def signup(userInput: SignupModal):
    print(userInput.Password)
    data = {
        "user_name": userInput.Name,
        "email": userInput.Email,
        "password_hash": hashPass(userInput.Password)
    }
    supabase.table("users").insert(data).execute()
    return {"m": 1}
