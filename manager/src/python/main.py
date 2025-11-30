from fastapi import FastAPI
import logging
from api.routes.routes import router
import uvicorn
from continous_loop import loop

# import your router from routes.py (expects a FastAPI APIRouter named `router`)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="darkwebsearch-manager", version="0.1.0")

# mount routes from routes.py
app.include_router(router)


@app.on_event("startup")
async def on_startup():
    logger.info("Application startup: initializing resources")
    loop.continious_loop()
    # Example: initialize DB/clients and store on app.state
    # app.state.db = await init_db()
    # app.state.http = httpx.AsyncClient()


@app.on_event("shutdown")
async def on_shutdown():
    logger.info("Application shutdown: cleaning up resources")
    # Example: cleanup/close connections
    # await app.state.db.close()
    # await app.state.http.aclose()


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
