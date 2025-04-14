import secrets

from sqlalchemy.ext.asyncio import AsyncSession

from app.common.exceptions import BadRequest, Unauthorized
from app.common.security import hash_password, verify_password
from app.user import models
from app.user.crud import UserCRUD, UserRefreshTokenCRUD
from app.user.schemas import base, create


async def create_user(data: create.UserCreate, db: AsyncSession):

    # Init crud
    user_crud = UserCRUD(db=db)

    # Check: If email exists
    if await user_crud.get(email=data.email):
        raise BadRequest(msg="User with email exists")

    # Create User
    user = await user_crud.create(
        data={
            "password": await hash_password(raw=data.password),
            **data.model_dump(exclude={"password"}),
        }
    )

    return user


async def login_user(credential: base.UserLoginCredentials, db: AsyncSession):

    # init Crud
    user_crud = UserCRUD(db=db)

    # Get use obj
    obj = await user_crud.get(email=credential.email)
    if not obj:
        raise Unauthorized("Invalid Login Credentials")

    # Verify password
    if not await verify_password(raw=credential.password, hashed=obj.password):
        raise Unauthorized("Invalid Login Credentials")

    return obj


async def create_user_refresh_token(user: models.User, db: AsyncSession):

    # Init crud
    ref_token_crud = UserRefreshTokenCRUD(db=db)

    # Create ref token
    ref_token_obj = await ref_token_crud.create(
        data={
            "user_id": user.id,
            "token": secrets.token_hex(),
        }
    )

    return ref_token_obj
