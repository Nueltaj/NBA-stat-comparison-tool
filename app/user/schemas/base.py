from datetime import datetime

from pydantic import BaseModel, EmailStr, Field

from app.common.schemas import Token


class User(BaseModel):
    """
    Base schemas for users
    """

    id: int = Field(description="The User's ID")
    pfp_url: str = Field(description="The url of the user's profile pic")
    first_name: str = Field(description="The User's first name")
    last_name: str = Field(description="The User's last name")
    email: str = Field(description="The User's email address")
    is_active: bool = Field(description="Whether the User is active or not")
    updated_at: datetime | None = Field(
        default=None, description="The User's last update date"
    )
    created_at: datetime = Field(description="The User's creation date")


class UserLoginCredentials(BaseModel):
    """
    Base schema for login credentials
    """

    email: EmailStr = Field(description="The User's email address")
    password: str = Field(description="The User's Raw password")


class UserLogin(BaseModel):
    """
    Base schema for user login response
    """

    user: User = Field(description="The user's details")
    tokens: Token = Field(description="The auth token")
