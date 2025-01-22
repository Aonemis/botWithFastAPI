from dotenv import load_dotenv
import os

load_dotenv()
DB_USERNAME=os.getenv("DB_USERNAME")
DB_PASSWORD=os.getenv("DB_PASSWORD")
DB_NAME=os.getenv("DB_NAME")
DATABASE_URL=f'postgresql+asyncpg://{DB_USERNAME}:{DB_PASSWORD}@localhost/{DB_NAME}'
BOT_TOKEN=os.getenv("BOT_TOKEN")