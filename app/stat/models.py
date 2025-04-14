from sqlalchemy import Column, Integer, String, Float

from app.core.database import DBBase


class Stat(DBBase):
    """
    Database Models for Stat
    """
    __tablename__ = "player_stats"

    id = Column(Integer, primary_key=True)
    player = Column(String, nullable=False)
    pts = Column(Float, nullable=False)
    ast = Column(Float, nullable=False)
    three_pt_pct = Column("three_pt_pct", Float, nullable=False)  # maps to 3P%
    fg_pct = Column("fg_pct", Float, nullable=False)  # maps to FG%
    trb = Column(Float, nullable=False)
    stl = Column(Float, nullable=False)
    blk = Column(Float, nullable=False)
    tov = Column(Float, nullable=False)
