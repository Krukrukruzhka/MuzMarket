from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from src.auth.router import router as router_auth
from src.catalog.router import router_catalog, router_main
from src.basket.router import router_basket
from src.delivery.router import router_delivery
from src.api.router import router as router_api


app = FastAPI()

app.mount("/src/templates/styles", StaticFiles(directory="src/templates/styles"), name="styles")
app.mount("/src/templates/images/icon", StaticFiles(directory="src/templates/images/icon"), name="icons")
app.mount("/src/templates/scripts", StaticFiles(directory="src/templates/scripts"), name="scripts")
app.mount("/src/src/items/instrument-images", StaticFiles(directory="src/src/items/instrument-images"), name="instrument_images")
app.mount("/src/templates/fonts", StaticFiles(directory="src/templates/fonts"), name="fonts")

app.include_router(router_catalog)
app.include_router(router_delivery)
app.include_router(router_basket)
app.include_router(router_auth)
app.include_router(router_main)
app.include_router(router_api)
