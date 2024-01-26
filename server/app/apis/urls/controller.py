from fastapi import status, HTTPException
from app.common.crawler import UrlCrawl
from app.core.exception import NotFoundException
from app.common.actions import check_url_exits
from app.common.exeptions import HttpxConnectionException


class UrlCrawlerController:
    @staticmethod
    async def get(db, request_body, user):
        crawl = UrlCrawl(request_body.url, db)
        try:
            crawl_result = await crawl.get_info()
        except HttpxConnectionException:
            raise HTTPException(
                detail="page not responding",
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )
        return crawl_result

    @staticmethod
    async def delete(db, url, user):
        crawl = UrlCrawl(url, db)
        exist = await check_url_exits(crawl.get_parsed_url(), db)
        if not exist:
            raise NotFoundException()
        await crawl.delete()
