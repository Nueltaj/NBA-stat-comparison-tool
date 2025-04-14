from pydantic import BaseModel, Field


class Stat(BaseModel):
    """
    Base model for Stats
    """

    id: int
    player: str = Field(example="LeBron James")
    pts: float = Field(example=27.5)
    ast: float = Field(example=8.1)
    three_pt_pct: float = Field(alias="3P%", example=38.2)
    fg_pct: float = Field(alias="FG%", example=52.7)
    trb: float = Field(example=7.4)
    stl: float = Field(example=1.6)
    blk: float = Field(example=0.9)
    tov: float = Field(example=3.5)

    class Config:
        orm_mode = True
