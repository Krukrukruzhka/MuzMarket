from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session
from src.api.router import get_regions
from sqlalchemy import text


router_basket = APIRouter(
    prefix="/basket",
    tags=["Basket"]
)

templates = Jinja2Templates(directory="src/templates")


@router_basket.get("/")
async def get_items(request: Request, regions=Depends(get_regions), session: AsyncSession = Depends(get_async_session)):
    try:
        return templates.TemplateResponse("basket.html", {"request": request,
                                                          "regions": regions})
    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "details": None
        })
