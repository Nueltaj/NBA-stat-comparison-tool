from pydantic import BaseModel, Field


class PlayerCompareRequest(BaseModel):
    """Schema for comparing two players"""

    player1: str = Field(..., example="LeBron James")
    player2: str = Field(..., example="Stephen Curry")


class PlayerStatRequest(BaseModel):
    player: str
