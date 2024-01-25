from abc import ABCMeta, abstractmethod
from bs4 import BeautifulSoup


class UrlCrawlABS(metaclass=ABCMeta):
    @abstractmethod
    async def _title(self, soup: BeautifulSoup) -> str:
        ...

    @abstractmethod
    async def _icon(self, soup: BeautifulSoup) -> str:
        ...

    @abstractmethod
    async def crawler(self, url: str) -> str:
        ...

    @abstractmethod
    async def delete(self, url: str) -> None:
        ...
