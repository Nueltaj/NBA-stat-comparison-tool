from pydantic import BaseModel, Field
from typing import Literal


class StatComparisonResponse(BaseModel):
    player1: str = Field(..., example="LeBron James")
    player2: str = Field(..., example="Stephen Curry")
    file_format: Literal["png", "pdf", "tiff", "jpg", "svg"] = Field(..., example="png")
    file_path: str = Field(
        ..., example="/plots/comparison_chart_of_lebron_james_to_stephen_curry.png"
    )
