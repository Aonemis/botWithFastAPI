import logging

from app.api.schemas import ProductCreate
from app.database.models import Product
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)

async def register_product(data: ProductCreate, session: AsyncSession):
    try:
        result = await session.execute(select(Product).where(Product.artikul==data.artikul))
        prod = result.scalar_one_or_none()
        if prod:
            prod.name=data.name
            prod.artikul=data.artikul
            prod.price=data.price
            prod.all_prod=data.all_prod
            prod.rating=data.rating
            logger.info(f"Update {prod}")
        else:
            prod = Product(
                name=data.name,
                artikul=data.artikul,
                price=data.price,
                all_prod=data.all_prod,
                rating=data.rating
            )
            session.add(prod)
            logger.info(f"Add new {prod}")
        await session.commit()
        logger.info("Commit in database")
    except Exception as e:
        await session.rollback()
        logger.info(f"Except {e}")
        raise e

"""
async def restart(session: AsyncSession):
    from app.api.endpoints import scheduler
    from app.services.utils import data_get
    result = await session.execute(select(SubscribeArtikul))
    arts = result.scalars().all()
    for a in arts:
        scheduler.add_job(data_get, id=f"{a.artikul}", trigger=IntervalTrigger(seconds=10), replace_existing=True,
                      kwargs={"artikul": a.artikul, "session": session})
"""

async def get_product(artikul: int, session: AsyncSession):
    try:
        result = await session.execute(select(Product).where(Product.artikul == artikul))
        prod = result.scalar_one_or_none()
        logger.info(f"Запрошенные данные по артикулу переданы пользователю")
        return {
            "name": prod.name,
            "artikul": artikul,
            "price": prod.price,
            "rating": prod.rating,
            "all_prod": prod.all_prod
        }
    except Exception as e:
        logger.info(f"Except {e}")
        print(e)
        return "Произошла ошибка при получении данных с БД"
