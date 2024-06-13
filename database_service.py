from typing import AsyncGenerator
from fastapi import HTTPException, status
from config import DB_PASS, DB_NAME, DB_USER, DB_HOST
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from models.models import Memes
from sqlalchemy import select, delete, update

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


async def exists_mem(object_name: str, session: AsyncSession):
    one_mem = select(Memes).where(Memes.object_name == object_name).limit(1)
    found = await session.scalars(one_mem)
    if found.all():
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Данное изображение уже существует")


async def add_mem(bucket_name: str, object_name: str, session: AsyncSession) -> None:
    mem = Memes(bucket_name=bucket_name, object_name=object_name)
    session.add(mem)
    await session.commit()
    await session.refresh(mem)


async def get_one_mem(pk: int, session: AsyncSession):
    mem = await session.execute(
        select(Memes).where(Memes.id == pk)
    )
    try:
        return mem.scalars().one_or_none().object_name
    except AttributeError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Изображение не найдено")


async def update_mem(pk: int, object_name: str, session: AsyncSession):
    await get_one_mem(pk, session)
    await session.execute(
        update(Memes)
        .where(Memes.id == pk)
        .values(object_name=object_name)
    )
    await session.commit()


async def del_mem(pk: int, session: AsyncSession):
    object_name = await get_one_mem(pk, session)
    await session.execute(
        delete(Memes)
        .where(Memes.id == pk)
    )
    await session.commit()
    return object_name
