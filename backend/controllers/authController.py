import os
from datetime import UTC, datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from models.auth import LoginModal, SignupModal, TokenData
from models.user import User
from passlib.context import CryptContext
from sqlmodel import Session, select
from tool.db import getSession

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
TOKEN_EXPIRATION_TIME_MINUTS = int(os.getenv("TOKEN_EXPIRATION_TIME_MINUTS"))

pwdContext = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()


def verifyPass(password, hashedPass):
    return pwdContext.verify(password, hashedPass)


def hashPass(password):
    return pwdContext.hash(password)


def getUser(userId, session: Session):
    try:
        return session.exec(select(User).where(User.id == userId)).first()
    except Exception as e:  # noqa: BLE001
        print(e)
        return None


def getUserFromEmail(email, session: Session):
    try:
        return session.exec(select(User).where(User.email == email)).first()
    except Exception as e:  # noqa: BLE001
        print(e)
        return None


def authenticateUser(email, password, session):
    user = getUserFromEmail(email, session)
    if not user:
        print(1)
        return False
    if not verifyPass(password, user.password_hash):
        print(0)
        return False

    return user


def createAccessToken(data, expiresDelta):
    toEncode = data.copy()
    expire = datetime.now(UTC) + expiresDelta

    toEncode["exp"] = expire
    encoded = jwt.encode(toEncode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded


async def getCurrentUser(
    credentials: HTTPAuthorizationCredentials = Depends(security),  # noqa: B008
    session: Session = Depends(getSession),  # noqa: B008
):
    token = credentials.credentials
    credentialException = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not authenticate the credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        userId = payload["sub"]
        if userId is None:
            raise credentialException
        tokenData = TokenData(id=userId)

    except JWTError as e:
        print(e)
        raise credentialException

    user = getUser(userId=tokenData.id, session=session)
    if user is None:
        raise credentialException

    return user


def loginController(userInput: LoginModal, session):
    user = authenticateUser(userInput.Email, userInput.Password, session)
    accessTokenExpire = timedelta(minutes=TOKEN_EXPIRATION_TIME_MINUTS)
    accessToken = createAccessToken(
        data={"sub": str(user.id)}, expiresDelta=accessTokenExpire
    )
    return {"access_token": accessToken, "token_type": "bearer"}


def signupController(userInput: SignupModal, session):
    user = User(
        user_name=userInput.Name,
        email=userInput.Email,
        password_hash=hashPass(userInput.Password),
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user
