from typing import Any

from pydantic import BaseModel, Field


class ResponseSchema(BaseModel):
    """This is the generic base response schema"""

    status: str = Field(description="The response status", default="success")
    msg: str = Field(default="Request Successful", description="The response message")
    data: Any = Field(description="The response data")


class Token(BaseModel):
    """
    Generic schema for tokens
    """

    type: str = "Bearer"
    access_token: str = Field(description="The access token")
    refresh_token: str = Field(description="The refresh token")
