from app.common.crawler import UrlCrawl
from app.core.exception import NotFoundException


class UrlCrawlerController:
    @staticmethod
    async def get(db, request_body, user):
        crawl = UrlCrawl(request_body.url, db)
        crawl_result = await crawl.crawler()
        return crawl_result

    @staticmethod
    async def delete(db, url, user):
        crawl = UrlCrawl(url, db)
        exist = await crawl.check_url_exits(crawl.pars_url())
        if not exist:
            raise NotFoundException()
        await crawl.delete()
