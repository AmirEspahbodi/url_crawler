from urllib.parse import urlparse
from httpx import (
    AsyncClient,
    ConnectTimeout,
    ConnectError,
    HTTPError,
    RequestError,
    TransportError,
    Response,
)
from app.common.exeptions import HttpxConnectionException


class UrlMixin:
    def pars_url(self, url):
        pars = urlparse(url)
        return {
            "domain": str(pars.hostname),
            "path": str(pars.path),
            "query_string": str(pars.query),
            "fragment": str(pars.fragment),
        }

    async def get_url(self, url, raise_exception=True) -> Response:
        try:
            async with AsyncClient() as client:
                response = await client.get(url)
                response.raise_for_status()
            return response
        except (
            ConnectTimeout,
            ConnectError,
            TimeoutError,
            HTTPError,
            RequestError,
            TransportError,
        ) as e:
            if raise_exception:
                raise HttpxConnectionException()
