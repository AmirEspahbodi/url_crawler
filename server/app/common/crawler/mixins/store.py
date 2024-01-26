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
from app.common.empty import Empty


class ImageMixin:
    def _image_response__store_in_disk(
        self,
        icon: Response | Empty,
    ) -> dict[str, str] | None:
        """
        create image instance in memory
        store it in file and return file path
        """
        image = Image.open(BytesIO(icon.content)).convert("RGBA")
        ts = time.time()
        filename = (
            "".join(
                random.choice(string.ascii_uppercase + string.digits) for _ in range(10)
            )
            + "_"
            + str(ts)
            + ".png"
        )
        directory = f"storage/"
        os.makedirs(directory, exist_ok=True)
        file_path = os.path.join(directory, filename)
        image.save(file_path, format="png")
        print("\n\n" + "111" * 50)
        print(file_path)
        print("\n\n")
        return file_path


class StoreMixin:
    async def _save_in_db(
        self,
        url_pars: dict[str, str],
        title: str,
        file_path: str,
    ):
        """
        save url in database
        """
        url_obj = Url(
            domain=url_pars["domain"],
            path=url_pars["path"],
            query_string=url_pars["query_string"],
            fragment=url_pars["fragment"],
            title=title,
            icon=file_path,
        )
        if not hasattr(self, "_db") or (hasattr(self, "_db") and self._db is None):
            async with async_session() as session:
                session.add(url_obj)
                await session.commit()
        else:
            self._db.add(url_obj)
            await self._db.commit()

        return url_obj.id
