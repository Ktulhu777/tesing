from typing import Callable, Any
import functools
import time

from fastapi import HTTPException
from minio import Minio
from fastapi_pagination.utils import disable_installed_extensions_check
from fastapi_pagination import paginate


def async_timed():
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapped(*args, **kwargs) -> Any:
            print(f'выполняется {func.__name__} с аргументами {args} {kwargs}')
            start = time.time()
            try:
                return await func(*args, **kwargs)
            finally:
                end = time.time()
                total = end - start
                print(f'{func} завершилась за {total:.4f} с')

        return wrapped

    return wrapper


def serialization_and_pagination(s3client: Minio):
    mem = []
    memes = {i.object_name: s3client.get_presigned_url(method="GET", bucket_name="test", object_name=i.object_name)
             for i in s3client.list_objects(bucket_name="test")}
    for key, value in memes.items():
        mem.append(
            {
                "object_name": key,
                "url": value
            }
        )

    disable_installed_extensions_check()

    return paginate(mem)


def validate_type_file(file):
    content_type = file.content_type
    if content_type not in ("image/jpeg", "image/png", "image/gif", "image/ico", 'image/webp', 'image/jpg'):
        raise HTTPException(status_code=400, detail="Invalid file type")
