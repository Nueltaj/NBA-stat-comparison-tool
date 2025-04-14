from pydantic import Field

from app.common.schemas import ResponseSchema
from app.user.schemas.base import User, UserLogin


class UserLoginResponse(ResponseSchema):
    """
    Response schema for user login
    """

    data: UserLogin = Field(description="The login details")


class UserResponse(ResponseSchema):
    """
    Response schema for users
    """

    msg: str = "User retrieved successfully"
    data: User = Field(description="The user's details")
