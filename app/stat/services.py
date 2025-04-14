import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Literal
from sqlalchemy.ext.asyncio import AsyncSession
from app.stat.models import Stat
from app.stat.schemas import create, response

# Load and prepare CSV once
FILENAME = "NBA_stat_2023_2024.csv"
df = pd.read_csv(FILENAME, encoding="latin-1")
df = df[["Player", "PTS", "AST", "3P%", "FG%", "TRB", "STL", "BLK", "TOV"]]
df.dropna(inplace=True)
df["Player"] = df["Player"].str.lower()
df.set_index("Player", inplace=True)

OUTPUT_FOLDER = "charts"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
SUPPORTED_FORMATS = ["png", "pdf", "tiff", "jpg", "svg"]


async def create_stat(request: create.PlayerCompareRequest, db: AsyncSession):
    player_key = request.player.lower().strip()

    if player_key not in df.index:
        raise ValueError("Player not found in stats CSV.")

    stats = df.loc[player_key]

    new_stat = Stat(
        player=request.player,
        pts=stats["PTS"],
        ast=stats["AST"],
        three_pt_pct=stats["3P%"],
        fg_pct=stats["FG%"],
        trb=stats["TRB"],
        stl=stats["STL"],
        blk=stats["BLK"],
        tov=stats["TOV"],
    )

    db.add(new_stat)
    await db.commit()
    await db.refresh(new_stat)

    return new_stat


async def get_player_stats(player: str):
    player = player.lower().strip()
    if player not in df.index:
        raise ValueError(f"Player '{player}' not found.")
    return df.loc[player]


async def generate_comparison_chart(player1: str, player2: str, file_format: Literal["png", "pdf", "tiff", "jpg", "svg"]) -> str:
    player1_data = await get_player_stats(player1)
    player2_data = await get_player_stats(player2)
    
    labels = ["PTS", "AST"]
    labels1 = ["TRB", "TOV"]
    labels2 = ["STL", "BLK"]
    labels3 = ["3P%", "FG%"]

    def make_df(keys):
        return pd.DataFrame({
            "stats": keys * 2,
            "values": np.concatenate([player1_data[keys].values, player2_data[keys].values]),
            "player": [player1] * len(keys) + [player2] * len(keys),
        })

    df_pts_ast = make_df(labels)
    df_reb_tov = make_df(labels1)
    df_stl_blk = make_df(labels2)
    df_shoot = make_df(labels3)

    fig, ax = plt.subplots(2, 2, figsize=(10, 6))
    sns.barplot(data=df_pts_ast, x="stats", y="values", hue="player", ax=ax[0, 0], palette="icefire")
    sns.barplot(data=df_reb_tov, x="stats", y="values", hue="player", ax=ax[0, 1], palette="cubehelix")
    sns.barplot(data=df_stl_blk, x="stats", y="values", hue="player", ax=ax[1, 0])
    sns.barplot(data=df_shoot, x="stats", y="values", hue="player", ax=ax[1, 1], palette="rocket_r")

    titles = [
        "(Points vs Assists)",
        "(Total Rebounds vs Turnovers)",
        "(Steals vs Blocks)",
        "(3P% vs FG%)"
    ]

    for i, title in enumerate(titles):
        ax[i // 2, i % 2].set_title(f"{player1.title()} vs {player2.title()} {title}", fontfamily="DejaVu Serif")
        ax[i // 2, i % 2].grid(axis="y", linestyle="--", alpha=0.6)

    plt.suptitle("NBA 2023/2024 Season Stats", fontfamily="DejaVu Serif", fontsize=15)
    plt.tight_layout()

    filename = f"comparison_chart_of_{player1}_to_{player2}.{file_format}"
    filepath = os.path.join(OUTPUT_FOLDER, filename)
    plt.savefig(filepath, format=file_format, dpi=300)
    plt.close()

    return filepath


async def compare_players_service(
    request: create.PlayerCompareRequest, file_format: str
):
    if file_format not in SUPPORTED_FORMATS:
        raise ValueError(f"Unsupported file format: {file_format}")

    filepath = await generate_comparison_chart(request.player1, request.player2, file_format)

    return response.StatComparisonResponse(
        player1=request.player1,
        player2=request.player2,
        file_format=file_format,
        file_path=f"/{filepath}",
    )
