from datetime import datetime
from sqlalchemy import select, or_
from sqlalchemy.orm import load_only
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.connection.database import async_session
from app.database import Url


async def check_url_exits(
    url: dict[str, str], db: AsyncSession | None = None
) -> dict[str, str] | None:
    stmt = (
        select(Url)
        .options(load_only(Url.id, Url.title, Url.icon))
        .where(Url.domain == url["domain"])
        .where(Url.path == url["path"])
        .where(Url.query_string == url["query_string"])
        .where(Url.fragment == url["fragment"])
        .where(or_(Url.valid_until >= datetime.now(), Url.valid_until == None))
        .where(Url.is_deleted == False)
    )
    result = None
    if db is None:
        async with async_session() as session:
            result = (await session.execute(stmt)).scalars().first()
    else:
        result = (await db.execute(stmt)).scalars().first()

    if result:
        return {
            "id": result.id,
            "title": result.title,
            "icon": result.icon,
        }
