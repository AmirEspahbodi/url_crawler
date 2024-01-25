import os
import time
import string
import random

from httpx import Response
from PIL import Image
from io import BytesIO
from sqlalchemy.ext.asyncio import AsyncSession


from app.database import Url
from app.core.connection.database import async_session
from app.common.image_url import image_url
from app.common.empty import empty


class StoreMixin:
    async def _save_in_db(
        self,
        url: dict[str, str],
        title: str,
        file_path: str,
        db: AsyncSession | None,
    ):
        url_obj = Url(
            domain=url["domain"],
            path=url["path"],
            query_string=url["query_string"],
            fragment=url["fragment"],
            title=str(title),
            icon=str(file_path),
        )
        if db is None:
            async with async_session() as session:
                session.add(url_obj)
                await session.commit()
        else:
            db.add(url_obj)
            await db.commit()
        return url_obj.id

    async def store(
        self,
        url: dict[str, str],
        title: str | empty,
        icon: Response | empty,
        db: AsyncSession | None = None,
    ) -> dict[str, str] | None:
        print("\n\n")
        print(f"title = {title}")
        print(f"icon = {icon}")
        image = (
            Image.open(BytesIO(icon.content)).convert("RGBA")
            if not icon is empty
            else empty
        )
        filename = "".join(
            random.choice(string.ascii_uppercase + string.digits) for _ in range(10)
        )
        ts = time.time()
        directory = f"storage/"
        os.makedirs(directory, exist_ok=True)
        file_path = os.path.join(
            directory,
            filename + "_" + str(ts) + ".png",
        )

        print(f"image = {image}")
        print("\n\n")
        if not image is empty:
            image.save(file_path, format="png")
        else:
            file_path = None

        url_id = await self._save_in_db(
            url,
            title,
            file_path,
            db,
        )

        return {
            "id": url_id,
            "title": str(title),
            "icon": image_url(file_path),
        }
