import asyncio
from requests_html import AsyncHTMLSession
import aiofiles
import os

path_to_save = '/home/dodo/Рабочий стол/repositories/aiogram3_conspect/async_html/exp'

if not os.path.exists(path_to_save ):
    os.mkdir(path_to_save )


async def save_page(html_content, index):
    filename = f"page_{index}.html"
    async with aiofiles.open(f'{path_to_save}/{filename}', "w", encoding="utf-8") as file:
        await file.write(html_content)

async def parse_page(url, index):
    session = AsyncHTMLSession()
    try:
        response = await session.get(url)
        await response.html.arender(scrolldown=20, sleep=0.1)
        html_content = response.html.html
        # сохраняем HTML в файл асинхронно
        await save_page(html_content, index)
        return html_content
    finally:
        await session.close()

async def parse_pages(urls):
    tasks = []
    for index, url in enumerate(urls):
        task = asyncio.create_task(parse_page(url, index))
        tasks.append(task)
    await asyncio.gather(*tasks)



urls = ['https://darwin.md/telefoane?page='+str(x) for x in range(1,10)]
asyncio.run(parse_pages(urls))
