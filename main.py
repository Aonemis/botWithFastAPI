import logging
from contextlib import asynccontextmanager
from aiogram.types import Update
from fastapi import FastAPI, Request
from app.api.endpoints import app_router, scheduler
from config.config import BOT_TOKEN, WEBHOOK_URL
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from tgBot.tgBot import router

logger = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
dp.include_router(router=router)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """logger.info("Start bot")
    await dp.start_polling(bot)
    await bot.delete_webhook(drop_pending_updates=True)
    yield
    await dp.stop_polling()"""

    webhook_url = WEBHOOK_URL
    await bot.set_webhook(url=webhook_url,
                          allowed_updates=dp.resolve_used_update_types(),
                          drop_pending_updates=True)
    logging.info(f"Webhook set to {webhook_url}")
    yield
    logging.info("Shutting down bot...")
    await bot.delete_webhook()
    logging.info("Webhook deleted")

logging.basicConfig(
        #filename='bot.log',
        #filemode='w',
        level=logging.INFO,
        format=f'[%(asctime)s] %(filename)s: %(name)s'
               f'%(lineno)d %(levelname)s %(message)s ')

logger.info("Start app")
scheduler.start()
app = FastAPI(lifespan=lifespan)
logger.info("Include router")
app.include_router(app_router)


@app.post("/webhook")
async def webhook(request: Request) -> None:
    update = Update.model_validate(await request.json(), context={"bot": bot})
    await dp.feed_update(bot, update)
    logging.info("Update processed")