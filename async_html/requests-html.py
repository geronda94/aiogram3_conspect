import asyncio
from requests_html import AsyncHTMLSession

async def get_number_of_pages(session, url):
    r = await session.get(url)
    await r.html.arender(sleep=0.1, keep_page=True, scrolldown=90)
    pagination = r.html.find('.pagination', first=True)
    pages = pagination.find('.page') if pagination else []
    return len(pages) or 1


async def get_product_urls(session, url):
    r = await session.get(url)
    await r.html.arender(sleep=0.1, keep_page=True, scrolldown=90)
    products = r.html.find('.product-card a.product-link')
    return [product.attrs['href'] for product in products]


async def parse_product(session, url):
    r = await session.get(url)
    await r.html.arender(sleep=0.1, keep_page=True, scrolldown=90)
    # парсинг информации о товаре
    product_data = {
        'title': r.html.find('.product-title', first=True).text,
        'description': r.html.find('.product-description', first=True).text,
        'price': r.html.find('.product-price', first=True).text,
        # ...
    }
    return product_data


async def main():
    # создаем сессию для асинхронных запросов
    session = AsyncHTMLSession()

    # получаем количество страниц и ссылки на все страницы
    main_url = 'https://example.com/products'
    num_pages = await get_number_of_pages(session, main_url)
    page_urls = [f'{main_url}?page={page}' for page in range(1, num_pages + 1)]

    # получаем ссылки на все товары
    product_urls = []
    for page_url in page_urls:
        product_urls += await get_product_urls(session, page_url)

    # парсим данные о каждом товаре
    products = await asyncio.gather(*[parse_product(session, url) for url in product_urls])

    # закрываем сессию
    await session.close()

    return products


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(main())
    print(results)
