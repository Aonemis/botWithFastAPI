import logging
from fastapi import FastAPI
from app.api.endpoints import app_router, scheduler

logger = logging.getLogger(__name__)

logging.basicConfig(
        #filename='bot.log',
        #filemode='w',
        level=logging.INFO,
        format=f'[%(asctime)s] %(filename)s: %(name)s'
               f'%(lineno)d %(levelname)s %(message)s ')

logger.info("Start app")
scheduler.start()
app = FastAPI()
logger.info("Include router")
app.include_router(app_router)

"""
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
dp.include_router(router)
"""