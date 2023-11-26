from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session
from sqlalchemy import text
from src.api.router import get_regions, get_item_by_article

router_catalog = APIRouter(
    prefix="/catalog",
    tags=["Catalog"]
)

router_main = APIRouter(
    prefix="",
    tags=["MainPage"]
)

templates = Jinja2Templates(directory="src/templates")


@router_catalog.get("/{instrument_subcategory}")
async def get_items(request: Request, instrument_subcategory: str, page: int = 1, regions=Depends(get_regions),
                    session: AsyncSession = Depends(get_async_session)):
    try:
        ELEMENTS_COUNT = 6
        query = f"""
            SELECT item.title AS title, price, rate, endpoint, article, subcategory.title AS subcategory FROM item
                INNER JOIN subcategory ON item.subcategory_id = subcategory.id
            WHERE subcategory.endpoint = "{instrument_subcategory}"
            ORDER BY rate DESC, price ASC
            LIMIT {ELEMENTS_COUNT} OFFSET {(page - 1) * ELEMENTS_COUNT};
        """
        items = await session.execute(text(query))

        query = f"""
            SELECT subcategory.title AS subcategory, category.title AS category, subcategory.endpoint AS endpoint FROM subcategory
                INNER JOIN category ON subcategory.category_id = category.id
            WHERE subcategory.endpoint = "{instrument_subcategory}";
        """
        subcategory_info = await session.execute(text(query))

        query = f"""
            SELECT DISTINCT
                strainer.title AS strainer_title, 
                parameter.title AS parameter_title
            FROM item
                INNER JOIN subcategory ON item.subcategory_id = subcategory.id
                INNER JOIN item_parameter ON item_parameter.item_id = item.id
                INNER JOIN parameter ON item_parameter.parameter_id = parameter.id
                INNER JOIN strainer ON strainer.id = parameter.strainer_id 
            WHERE subcategory.endpoint = "{instrument_subcategory}";
        """
        parameters_info = await session.execute(text(query))
        parameters_info = parameters_info.all()
        strainers = set(map(lambda x: x[0], parameters_info))
        strainers = {i: [] for i in sorted(strainers)}
        for i in parameters_info:
            strainers[i[0]].append(i[1])

        return templates.TemplateResponse("catalog.html", {"request": request,
                                                           "items": items.all(),
                                                           "strainers": strainers,
                                                           "subcategory_info": subcategory_info.fetchone(),
                                                           "regions": regions})
    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "details": None
        })


@router_catalog.get("/{instrument_subcategory}/{article}")
async def get_items(request: Request,
                    instrument_subcategory: str, article: str,
                    regions=Depends(get_regions), item=Depends(get_item_by_article),
                    session: AsyncSession = Depends(get_async_session)):
    try:
        # query = f"""
        #     SELECT
        #         subcategory.title AS subcategory, endpoint,
        #         item.title AS title, price, rate, article,
        #         parameter.title AS parameter,
        #         strainer.title AS strainer
        #     FROM item
        #         INNER JOIN subcategory ON subcategory.id = item.subcategory_id
        #         INNER JOIN item_parameter ON item_parameter.item_id = item.id
        #         LEFT JOIN parameter ON parameter.id = item_parameter.parameter_id
        #         INNER JOIN strainer ON strainer.id = parameter.strainer_id
        #     WHERE endpoint = "{instrument_subcategory}" AND article = "{instrument_article}";
        # """
        # items = await session.execute(text(query))
        # items = items.all()
        # if len(items) == 0:
        #     raise
        # items = {
        #     "title": items[0][2],
        #     "subcategory": items[0][0],
        #     "endpoint": items[0][1],
        #     "price": items[0][3],
        #     "rate": items[0][4],
        #     "article": items[0][5],
        #     "parameters": {item[7]: item[6] for item in items}
        # }
        # return items
        # query = f"""
        #     SELECT DISTINCT
        #         strainer.title AS strainer_title,
        #         parameter.title AS parameter_title
        #     FROM item
        #         INNER JOIN subcategory ON item.subcategory_id = subcategory.id
        #         INNER JOIN item_parameter ON item_parameter.item_id = item.id
        #         INNER JOIN parameter ON item_parameter.parameter_id = parameter.id
        #         INNER JOIN strainer ON strainer.id = parameter.strainer_id
        #     WHERE subcategory.endpoint = "{instrument_subcategory}";
        # """
        # parameters_info = await session.execute(text(query))
        # parameters_info = parameters_info.all()
        # strainers = set(map(lambda x: x[0], parameters_info))
        # strainers = {i:[] for i in sorted(strainers)}
        # for i in parameters_info:
        #     strainers[i[0]].append(i[1])

        return templates.TemplateResponse("product.html", {"request": request,
                                                           "item": item,
                                                           # "strainers": strainers,
                                                           # "subcategory_info": subcategory_info.fetchone(),
                                                           "regions": regions})
    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "details": None
        })


@router_main.get("/")
async def get_catalog_page(request: Request, regions=Depends(get_regions),
                           session: AsyncSession = Depends(get_async_session)):
    ELEMENTS_COUNT = 6
    query = f"""
                SELECT item.title AS title, price, rate, article, subcategory.title AS subcategory, endpoint FROM item
                    INNER JOIN subcategory ON item.subcategory_id = subcategory.id
                ORDER BY rate DESC
                LIMIT {ELEMENTS_COUNT};
            """
    items = await session.execute(text(query))

    query = f"""
                SELECT subcategory.title AS title, category.title AS category, endpoint FROM subcategory
                    INNER JOIN category ON subcategory.category_id = category.id;
            """
    subcategories = await session.execute(text(query))
    categories = dict()
    for i in subcategories.all():
        categories[i[1]] = categories.get(i[1], []) + [{'title': i[0], 'endpoint': i[2]}]
    return templates.TemplateResponse("index.html", {"request": request,
                                                     "items": items.all(),
                                                     "categories": categories,
                                                     "regions": regions})

# @router_main.get()
