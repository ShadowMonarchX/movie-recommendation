from fastapi import  FastAPI
from pydantic import BaseModel
import asyncio





class Item(BaseModel):
    id : int
    enrollment_no = int
    name: str
    math: float | None = 0
    phy: float | None = 0
    che: float | None = 0
    eng: float | None = 0
    email: str | None = None
    img: str | None = None



