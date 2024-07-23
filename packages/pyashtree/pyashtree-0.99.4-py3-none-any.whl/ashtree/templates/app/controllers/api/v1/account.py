from typing import Optional, Literal, Annotated
from pydantic import BaseModel
from pydantic.functional_validators import AfterValidator
from fastapi import APIRouter, Depends, Body
from datetime import datetime
from ashtree.errors import AuthenticationError, BadRequest
from app.extractors import authenticated_user, current_session
from app.models import User, Session

account_ctrl = APIRouter(prefix="/api/v1/account")


class AccountMeResponse(BaseModel):
    id: Annotated[Optional[str], AfterValidator(str)]
    username: str
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]
    ext_id: Optional[str]
    avatar_url: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class LogoutResponse(BaseModel):
    detail: Literal["logged out"] = "logged out"


class AuthenticationRequest(BaseModel):
    username: str
    password: str



@account_ctrl.get("/me")
async def me(user: User = Depends(authenticated_user())) -> AccountMeResponse:
    return AccountMeResponse(**user.to_dict())


@account_ctrl.post("/authenticate")
async def authenticate(
        auth_request: AuthenticationRequest = Body(),
        session: Session = Depends(current_session)) -> AccountMeResponse:

    user = await session.user()
    if user:
        raise BadRequest("already authenticated")

    user = await User.get(auth_request.username)
    if user is None or not user.check_password(auth_request.password):
        raise AuthenticationError()
    session.user_id = user.id

    return AccountMeResponse(**user.to_dict())


@account_ctrl.post("/logout")
async def logout(session: Session = Depends(current_session)) -> LogoutResponse:
    session.user_id = None
    return LogoutResponse(detail="logged out")
