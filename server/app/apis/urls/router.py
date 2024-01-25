from fastapi import APIRouter, Depends, status, Security, Query
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.schema.validate import Validate
from app.core.connection.database import connection
from app.core.security.check_auth import AuthenticationRequired

from .controller import UrlCrawlerController as url
from .schema import UrlResponseSchema, UrlRequestSchema

url_router = APIRouter()


@url_router.post(
    "/get",
    status_code=status.HTTP_200_OK,
    summary="get url info",
    response_model=UrlResponseSchema,
)
async def get_url(
    request_body: UrlRequestSchema,
    db: Annotated[AsyncSession, Depends(connection)],
    user: Annotated[
        dict[str, int | bool | str],
        Security(AuthenticationRequired.check_auth),
    ],
):
    """
    get url info.
    """

    validation_result = await Validate().validate(request_body, db=db)
    result = await url.get(db, request_body, user)
    return result


@url_router.delete(
    "/delete",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="delete url info",
)
async def get_url(
    db: Annotated[AsyncSession, Depends(connection)],
    user: Annotated[
        dict[str, int | bool | str],
        Security(AuthenticationRequired.check_auth),
    ],
    query: Annotated[str, Query()],
):
    """
    delete url info.
    """

    await url.delete(db, query, user)
