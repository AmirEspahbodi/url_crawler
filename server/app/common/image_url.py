from app.core.config import AppConfig


def image_url(file_path: str):
    if file_path is None:
        return
    return AppConfig.BASE_URL + "/" + file_path.replace("\\", "/")
