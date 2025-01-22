import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from fastapi import APIRouter, Body, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.db import get_session
from app.services.dao import get_product
from app.services.utils import data_get

logger = logging.getLogger(__name__)
scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
app_router = APIRouter(prefix='/api/v1', tags=['api'])

@app_router.post('/products')
async def get_products(data: dict = Body(), session: AsyncSession = Depends(get_session)):
    try:
        result = await data_get(data["artikul"], session)
        return result
    except Exception as e:
        logger.info(f"Except {e}")
        return HTTPException(status_code=404, detail="Atrikul not found")

@app_router.get("/subscribe/{artikul}")
async def reload_product(artikul: int, session: AsyncSession = Depends(get_session)):
        try:
            result = await data_get(artikul, session)
            scheduler.add_job(data_get, id=f"{artikul}", trigger=IntervalTrigger(seconds=10), replace_existing=True, kwargs={"artikul": artikul,"session": session})
            return {"Success register one_on_30 minute prod:": result}
        except Exception as e:
            logger.info(f"Except {e}")
            return HTTPException(status_code=404, detail="Atrikul not found or can't register job")


"""
@app_router.get("/info/{artikul}")
async def get_prod_info(artikul: int, session: AsyncSession = Depends(get_session)):
    result = await get_product(artikul, session)
    return {"result": result}
"""