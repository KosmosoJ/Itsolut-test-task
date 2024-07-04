from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import os 
from dotenv import find_dotenv,load_dotenv


if find_dotenv():
    load_dotenv()

if os.getenv('DB_PATH'):
    DB_PATH = os.getenv('DB_PATH')
else:
    DB_PATH = 'postgresql+asyncpg://postgres:postgres@db:5432/itsolut'

try:
    engine = create_async_engine(DB_PATH, echo=True)
except Exception:
    exit('Не удалось создать движок')


async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session 
