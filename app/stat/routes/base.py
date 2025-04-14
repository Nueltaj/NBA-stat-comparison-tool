from fastapi import APIRouter, HTTPException
from app.stat.schemas import base, create, response
from app.common.annotations import DatabaseSession
from app.stat.services import create_stat, compare_players_service, generate_comparison_chart


router = APIRouter()

SUPPORTED_FORMATS = ["png", "pdf", "tiff", "jpg", "svg"]


@router.post("/create", response_model=base.Stat)
async def route_create_stat(req: create.PlayerStatRequest, db: DatabaseSession):
    """
    Create a new player stat
    """
    try:
        return await create_stat(req, db)
    except ValueError as e:
        print(e)


@router.post("/compare", response_model=response.StatComparisonResponse)
async def route_compare_players(req: create.PlayerCompareRequest, file_format: str):
    if file_format not in SUPPORTED_FORMATS:
        raise HTTPException(
            status_code=400, detail=f"Unsupported file format: {file_format}"
        )

    filepath = await generate_comparison_chart(req.player1, req.player2, file_format)

    return response.StatComparisonResponse(
        player1=req.player1,
        player2=req.player2,
        file_format=file_format,
        file_path=f"/{filepath}"
    )