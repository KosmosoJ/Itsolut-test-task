from bs4 import BeautifulSoup
import aiohttp
import asyncio
from fastapi import HTTPException
from .adverts import create_advert
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Advert


headers = {
        'accept':'"text/html"',
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0'
    }

async def get_page_data(session,item, position, db_session:AsyncSession):
    """ Парсим конкретную ссылку и достаем оттуда информацию по опубликованному на сайте объявлению """
    async with session.get(url=item['link'].strip(), headers=headers) as response:
        soup = BeautifulSoup(await response.text(), 'lxml')
        title = soup.find('h1', class_='subject').text.strip()
        author = soup.find('span', class_='userNick').text.strip()
        id = soup.find('span', class_ = 'viewbull-bulletin-id__num').string.strip()
        views = item['views']
        print(title, author, views ,id, position)
    advert_info = {'title':title, 'author':author,'views':views, 'id':id,'position':position}
    advert = await create_advert(advert_info, db_session)
    
    return advert

async def gather_data(db_session:AsyncSession) -> list[Advert]:
    """ Собираем объявления указанные на сайте """
    url = 'https://www.farpost.ru/vladivostok/service/construction/guard/+/%D0%A1%D0%B8%D1%81%D1%82%D0%B5%D0%BC%D1%8B+%D0%B2%D0%B8%D0%B4%D0%B5%D0%BE%D0%BD%D0%B0%D0%B1%D0%BB%D1%8E%D0%B4%D0%B5%D0%BD%D0%B8%D1%8F/#center=43.172967176037695%2C131.96034531052942&zoom=11'
    
    async with aiohttp.ClientSession() as session:
        response = await session.get(url=url, headers = headers)
        if response.status == 200:
            soup = BeautifulSoup(await response.text(), 'lxml')
            items = {}
            for id, item in enumerate(soup.find_all('tr', class_='bull-list-item-js')[:10]):
                item_soup = item
                views = item_soup.find('span', class_='views').string
                link = item_soup.find('a', class_='bulletinLink', href=True)
                
                items[id+1] = {'views':views, 'link':'https://www.farpost.ru'+link['href']}

            result = []
            if len(items) > 0:
                
                for item in items:
                    item_result = await get_page_data(session,items[item],item,db_session)
                    result.append(item_result)

            else:
                raise HTTPException(404, 'Уткнулись в лимит запросов на сайт')
                exit('Уткнулись в лимит запросов')

    return result

if __name__ == '__main__':
    """ Используется для запуска скрипта вне fastapi приложения """
    asyncio.run(gather_data())