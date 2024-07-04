from bs4 import BeautifulSoup
import aiohttp
import asyncio

headers = {
        'accept':'"text/html"',
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0'
    }

async def get_page_data(session:aiohttp.ClientSession, link):
    response = await session.get(link, headers=headers)
    soup = BeautifulSoup(await response.text(), 'lxml')
    title = soup.find('h1', class_='subject').string
    author = soup.find('span', class_='userNick').string
    id = soup.find('span', class_ = 'viewbull-bulletin-id__num').string
    views = link['views']
    print(title, author, views ,id)
    #TODO создание модели

async def gather_data():
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

                items[id] = {'views':views, 'link':'www.farpost.ru' + link['href']}

            tasks = []
            for item in items:
                task = asyncio.create_task(get_page_data(session, item))
                tasks.append(task)
            await asyncio.gather(*tasks)