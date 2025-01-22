import requests
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas import ProductCreate
from app.services.dao import register_product

url_wb = 'https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&dest=-1257786&spp=30&nm='

async def data_get(artikul: int, session: AsyncSession):
    try:
        req = requests.get(url=f'{url_wb}{artikul}')
        req = dict(req.json())
        name = req['data']['products'][0]['name']
        price = req['data']['products'][0]['salePriceU']/100
        rating = req['data']['products'][0]['reviewRating']
        all_prod = req['data']['products'][0]['totalQuantity']
        result = ProductCreate(
            name = name,
            artikul = artikul,
            price = price,
            rating = rating,
            all_prod = all_prod
        )
        await register_product(result, session)
        return result
    except Exception as e:
        raise e

