import os

import uvicorn
from fastapi import FastAPI, UploadFile, Depends, File
from sqlalchemy.ext.asyncio import AsyncSession
from s3client import s3client
from fastapi_pagination import Page, add_pagination
from schema.schema import MemesGetAll
from utils import serialization_and_pagination, validate_type_file  # async_timed
from database_service import (add_mem, exists_mem,
                              get_one_mem, get_async_session,
                              del_mem, update_mem)


app = FastAPI(title="MEMES")
add_pagination(app)


@app.get("/memes/", response_model=Page[MemesGetAll])  # ?page=1&size=10
def get_memes():
    return serialization_and_pagination(s3client)


@app.get("/memes/{pk}/")
async def get_memes(pk: int, session: AsyncSession = Depends(get_async_session)):
    object_name = await get_one_mem(pk, session)
    response = s3client.get_presigned_url(method="GET", bucket_name="test", object_name=object_name)
    return {"url": response}


@app.post("/memes/")
async def post_memes(file: UploadFile = File(...), session: AsyncSession = Depends(get_async_session)):
    validate_type_file(file)
    await exists_mem(object_name=file.filename, session=session)
    await add_mem(bucket_name="test", object_name=file.filename, session=session)
    file_size = os.fstat(file.file.fileno()).st_size
    s3client.put_object('test', file.filename, file.file, file_size)
    return {"success": "Фотография успешно сохранена."}


@app.put("/memes/{pk}/")
async def put_memes(pk: int,
                    file: UploadFile = File(...),
                    session: AsyncSession = Depends(get_async_session)):
    validate_type_file(file)
    await update_mem(pk, file.filename, session)
    file_size = os.fstat(file.file.fileno()).st_size
    s3client.put_object('test', file.filename, file.file, file_size)
    return {"success": "Фотография успешно обновлена."}


@app.delete("/memes/{pk}/")
async def delete_memes(pk: int, session: AsyncSession = Depends(get_async_session)):
    object_name = await del_mem(pk, session)
    s3client.remove_object("test", object_name)
    return {"success": "Изображение удалено!"}


if __name__ == "__main__":
    uvicorn.run(app=app, port=5000)
