from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Header
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.annotations import DatabaseSession
from app.common.exceptions import Forbidden, Unauthorized
from app.core.settings import get_settings
from app.user.auth import UserTokenGenerator
from app.user.crud import UserCRUD, UserRefreshTokenCRUD
from app.user.exceptions import UserNotFound

# Globals
settings = get_settings()
token_gen = UserTokenGenerator()


async def get_user_by_id(
    id: int, db: AsyncSession, raise_exc: bool = True, return_active: bool = True
):

    # init CRUD
    user_crud = UserCRUD(db=db)

    # get user by id
    user = await user_crud.get(id=id)

    # Check: user not found
    if not user and raise_exc:
        raise UserNotFound()

    # Check: inactive user
    if user and not bool(user.is_active) and return_active:
        raise Forbidden("User has been deactivated")

    return user


async def get_current_user(
    token: Annotated[str, Header(alias="Authorization")],
    db: DatabaseSession,
):

    # Split token
    try:
        token = token.split()[1]
    except KeyError:
        raise Unauthorized("Invalid token")

    # Verify token
    user_id = await token_gen.verify(token=token, sub_head="USER", db=db)

    # Check: valid user id
    user = await get_user_by_id(id=int(user_id), db=db)

    return user


#####################################################################
# USER REFRESH TOKEN
#####################################################################
async def get_user_refresh_token(token: str, db: AsyncSession):

    # Init crud
    ref_token_crud = UserRefreshTokenCRUD(db=db)

    # Get ref token
    ref_token = await ref_token_crud.get(token=token)

    # Check: exists
    if not ref_token:
        raise Unauthorized("Refresh token not found")

    # Check: expired
    token_expires_at: datetime = ref_token.created_at + timedelta(
        hours=settings.REFRESH_TOKEN_EXPIRE_HOUR  # type: ignore
    )
    if datetime.now() > token_expires_at.replace(tzinfo=None):
        raise Unauthorized("Refresh token has expired")

    return ref_token
