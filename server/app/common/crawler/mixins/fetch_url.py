from httpx import AsyncClient, ConnectTimeout
from bs4 import BeautifulSoup


class CrawleMixin:
    async def fetch_url(self, url):
        try:
            async with AsyncClient() as client:
                page = await client.get(url)
            return page
        except ConnectTimeout as e:
            print(e)

    async def get_soup(self, url, features="html.parser"):
        page = await self.fetch_url(url)
        if page is not None:
            return BeautifulSoup(page.text, features)
