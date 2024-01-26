from bs4 import BeautifulSoup
from httpx import Response
from sqlalchemy import update, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.connection.database import async_session
from app.database import Url
from app.common.actions import check_url_exits
from app.common.empty import Empty

from .base import UrlCrawlABS
from .mixins import ImageMixin, UrlMixin, StoreMixin


class UrlCrawl(UrlCrawlABS, ImageMixin, UrlMixin, StoreMixin):
    _db: AsyncSession | None
    _url: str
    _url_pars: str

    def __init__(self, url: str, db: AsyncSession | None = None) -> None:
        self._url = url
        self._url_pars = self.pars_url(url)
        if db:
            self._db = db

    def set_url(self, url):
        self._url = url
        self._url_pars = self.pars_url(url)

    def get_parsed_url(self):
        return self._url_pars

    def _title(self, soup: BeautifulSoup) -> str:
        """
        return web page title if exist if not return Empty class
        """
        title_tag = soup.find("title")
        if title_tag is None:
            return Empty
        if title_tag.contents is None:
            return Empty
        return title_tag.contents

    async def _icon(self, soup: BeautifulSoup) -> Response:
        """
        return web page icon if exist if not return Empty class
        """
        icon_tag = soup.find("link", rel=("icon", "shortcut icon"))
        if icon_tag is None:
            return Empty
        icon_link = icon_tag["href"]
        if icon_link.startswith("/") or icon_link.startswith("."):
            icon_link = f"{self._url}{icon_link}"
        print(icon_link)
        icon = await self.get_url(icon_link, raise_exception=False)
        if icon is None:
            return Empty

    async def _crawl(self) -> str:
        """
        crawl url get title and icon
        store icon in disk
        return title and icon path
        """

        # get web page
        web_page: Response = await self.get_url(self._url)

        # make soup
        soup = BeautifulSoup(web_page.text, "html.parser")

        # get web page title
        title = self._title(soup)

        # get icon in http response
        icon_in_resopnse = await self._icon(soup)

        icon_path = Empty
        if icon_in_resopnse is not Empty:
            # build Image in and store it in disk and return file path (in storage directory)
            icon_path = self._image_response__store_in_disk(icon_in_resopnse)

        return {
            "title": str(title),
            "icon_path": icon_path if not Empty else "",
        }

    async def get_info(self) -> dict[str, str]:
        """
        check valid info exist in database end return it
        if not crawl url and save in in database
        """
        exist = await check_url_exits(self._url_pars)
        if exist:
            return exist

        crawl_result = await self._crawl()
        db_url_id = await self._save_in_db(
            url_pars=self._url_pars,
            file_path=crawl_result["icon_path"],
            title=crawl_result["title"],
        )
        return {
            "id": db_url_id,
            "icon": crawl_result["icon_path"],
            "title": crawl_result["title"],
        }

    async def delete(self) -> None:
        stmt = (
            update(Url)
            .where(Url.domain == self._url_pars["domain"])
            .where(Url.path == self._url_pars["path"])
            .where(Url.query_string == self._url_pars["query_string"])
            .where(Url.fragment == self._url_pars["fragment"])
            .where(Url.is_deleted == False)
        ).values(
            is_deleted=True,
            deleted_at=func.now(),
        )
        if self._db is None:
            async with async_session() as session:
                await session.execute(stmt)
                await session.commit()
        else:
            await self._db.execute(stmt)
            await self._db.commit()


# test
# url_crawler = UrlCrawl("https://www.geeksforgeeks.org/extract-title-from-a-webpage-using-python/")
# asyncio.run(
#     url_crawler.get_info()
# )
