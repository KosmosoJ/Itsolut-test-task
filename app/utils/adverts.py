from database.models import Advert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException


async def create_advert(advert_info:dict,session:AsyncSession) -> Advert:
    new_advert = Advert(farpost_id = int(advert_info['id'][1:]), author = advert_info['author'],
                        views = int(advert_info['views']), position = int(advert_info['position']))
    session.add(new_advert)
    await session.commit()
    return new_advert


async def get_advert_from_db(id:int, session:AsyncSession) -> Advert:
    advert = await session.execute(select(Advert).where(Advert.id == id))
    advert = advert.scalars().first()
    if not advert:
        raise HTTPException(404, f"Не нашли объявление с id '{id}'")
    return advert

async def get_adver_from_db_farpost_id(farpost_id:int, session:AsyncSession) -> Advert:
    advert = await session.execute(select(Advert).where(Advert.farpost_id == farpost_id))
    advert = advert.scalars().first()
    if not advert:
        raise HTTPException(404, f"Не нашли объявление с id '{farpost_id}'")
    return advert 


