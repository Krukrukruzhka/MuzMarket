from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session
from sqlalchemy import text
from src.auth.auth import current_user
from src.auth.models import User


router = APIRouter(
    prefix="/api",
    tags=["API"]
)


@router.get("/regions")
async def get_regions(session: AsyncSession = Depends(get_async_session)):
    query = "SELECT title FROM region;"
    regions = await session.execute(text(query))
    regions = ["Москва", "Санкт-Петербург"] + sorted([region[0] for region in regions.all() if region[0] not in ["Москва", "Санкт-Петербург"]])
    return regions


@router.get("/my_orderings")
async def get_orderings(user: User = Depends(current_user), session: AsyncSession = Depends(get_async_session)):
    query = f"""
        SELECT
            store_id AS store, item.title AS item, amount, timestamp, status.title AS status, price, ordering.id AS id
        FROM ordering 
            INNER JOIN user ON user.id = ordering.user_id 
            INNER JOIN status ON status.id = ordering.status_id
            INNER JOIN item ON item.id = ordering.item_id
        WHERE user.id = {user.id};"""
    orderings = await session.execute(text(query))
    return orderings.all()


@router.get("/instrument/{article}")
async def get_item_by_article(article: str, session: AsyncSession = Depends(get_async_session)):
    query = f"""
                SELECT 
                    subcategory.title AS subcategory, endpoint, 
                    item.title AS title, price, rate, article,
                    parameter.title AS parameter,
                    strainer.title AS strainer
                FROM item
                    INNER JOIN subcategory ON subcategory.id = item.subcategory_id
                    INNER JOIN item_parameter ON item_parameter.item_id = item.id
                    LEFT JOIN parameter ON parameter.id = item_parameter.parameter_id
                    INNER JOIN strainer ON strainer.id = parameter.strainer_id
                WHERE article = "{article}";
            """
    items = await session.execute(text(query))
    items = items.all()
    if len(items) == 0:
        raise
    items = {
        "title": items[0][2],
        "subcategory": items[0][0],
        "endpoint": items[0][1],
        "price": items[0][3],
        "rate": items[0][4],
        "article": items[0][5],
        "parameters": {item[7]: item[6] for item in items}
    }
    return items


@router.get("/my_data")
async def get_user_data(user: User = Depends(current_user)):
    return user.__dict__
