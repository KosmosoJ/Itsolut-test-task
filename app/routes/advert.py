from fastapi import APIRouter, Depends
from database.db import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from utils.parse import gather_data
import utils.adverts as adverts_utils

router = APIRouter()

@router.get('/get_adverts/')
async def get_adverts_from_farpost(session: AsyncSession = Depends(get_session)):
    adverts = await gather_data(session)
    return [{'id':a.id, 'farpost_id':a.farpost_id, 'author':a.author, 'views':a.views,
             'position':a.position, 'gathered_at':a.gathered_at} for a in adverts]

@router.get('/get_advert/{id}')
async def get_advert_with_farpost_id(id:int, session:AsyncSession = Depends(get_session)):
    advert = await adverts_utils.get_advert_from_db(id, session)
    return {'id':advert.id, 'farpost_id':advert.farpost_id, 'author':advert.author, 'views':advert.views,
            'position':advert.position, 'gathered_at':advert.gathered_at}
    

@router.get('/get_farpost_advert/{id}')
async def get_advert_with_id(id:int, session:AsyncSession = Depends(get_session)):
    advert = await adverts_utils.get_adver_from_db_farpost_id(id, session)
    return {'id':advert.id, 'farpost_id':advert.farpost_id, 'author':advert.author, 'views':advert.views,
            'position':advert.position, 'gathered_at':advert.gathered_at}