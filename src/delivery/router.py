from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session
from src.api.router import get_regions, get_orderings

router_delivery = APIRouter(
    prefix="/delivery",
    tags=["Delivery"]
)

templates = Jinja2Templates(directory="src/templates")


@router_delivery.get("/")
async def get_items(request: Request, regions=Depends(get_regions), orderings=Depends(get_orderings)):
    try:
        return templates.TemplateResponse("delivery.html", {"request": request,
                                                            "regions": regions,
                                                            "active_orderings": [ordering for ordering in orderings if ordering.status == 'В доставке'],
                                                            "orderings": orderings})
    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "details": None
        })
