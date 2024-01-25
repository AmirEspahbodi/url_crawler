import asyncio

from bs4 import BeautifulSoup
from httpx import Response
from urllib.parse import urlparse
from sqlalchemy import select, update, func
from sqlalchemy.orm import load_only
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.connection.database import async_session
from app.common.empty import empty
from app.database import Url
from app.common.image_url import image_url

from .base import UrlCrawlABS
from .mixins import CrawleMixin, StoreMixin


class UrlCrawl(UrlCrawlABS, CrawleMixin, StoreMixin):
    db: AsyncSession | None
    url: str

    def __init__(self, url: str, db: AsyncSession | None = None) -> None:
        self.url = url
        if db:
            self.db = db

    def _title(self, soup: BeautifulSoup) -> str:
        title_tag = soup.find("title")
        if title_tag is None:
            return empty
        if title_tag.contents is None:
            return empty
        return title_tag.contents

    async def _icon(self, soup: BeautifulSoup) -> Response:
        icon_tag = soup.find("link", rel=("icon", "shortcut icon"))
        if icon_tag is None:
            return empty
        icon_link = icon_tag["href"]
        if icon_link.startswith("/") or icon_link.startswith("."):
            icon_link = f"{self.url}{icon_link}"
        return await self.fetch_url(icon_link)

    async def check_url_exits(self, url: dict[str, str]) -> dict[str, str] | None:
        stmt = (
            select(Url)
            .options(load_only(Url.id, Url.title, Url.icon))
            .where(Url.domain == url["domain"])
            .where(Url.path == url["path"])
            .where(Url.query_string == url["query_string"])
            .where(Url.fragment == url["fragment"])
            .where(Url.is_deleted == False)
        )
        result = None
        if self.db is None:
            async with async_session() as session:
                result = (await session.execute(stmt)).scalars().first()
        else:
            result = (await self.db.execute(stmt)).scalars().first()

        if result:
            return {
                "id": result.id,
                "title": result.title,
                "icon": image_url(result.icon),
            }

    def pars_url(self):
        pars = urlparse(self.url)
        return {
            "domain": pars.hostname,
            "path": pars.path,
            "query_string": pars.query,
            "fragment": pars.fragment,
        }

    async def crawler(self) -> str:
        url_pars = self.pars_url()
        exist = await self.check_url_exits(url_pars)
        if exist:
            return exist

        soup = await self.get_soup(self.url)
        if soup is None:
            print("connection error")
            return
        title = self._title(soup)
        icon = await self._icon(soup)
        if icon is None:
            print("connection error")
            return

        if icon is empty:
            pass

        result = await self.store(url_pars, title, icon, db=self.db)
        return result

    async def delete(self) -> None:
        url_pars = self.pars_url()
        stmt = (
            update(Url)
            .where(Url.domain == url_pars["domain"])
            .where(Url.path == url_pars["path"])
            .where(Url.query_string == url_pars["query_string"])
            .where(Url.fragment == url_pars["fragment"])
            .where(Url.is_deleted == False)
        ).values(
            is_deleted=True,
            deleted_at=func.now(),
        )
        async with async_session() as session:
            await session.execute(stmt)
            await session.commit()


# test
# url_crawler = UrlCrawl()
# asyncio.run(
#     url_crawler.crawler(
#         "https://www.geeksforgeeks.org/extract-title-from-a-webpage-using-python/"
#     )
# )
