# app_book_author/crud.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from . import models, schemas


# --- Authors ---
async def create_author(db: AsyncSession, author: schemas.AuthorCreate):
    db_author = models.Author(**author.model_dump())
    db.add(db_author)
    await db.commit()
    await db.refresh(db_author)
    return db_author

async def read_authors(db: AsyncSession):
    result = await db.execute(select(models.Author))
    return result.scalars().all()

async def update_author_name(db: AsyncSession, author_id: int, new_name: str):
    author = await db.get(models.Author, author_id)
    if author:
        author.name = new_name
        await db.commit()
        await db.refresh(author)
    return author

# --- Books ---
async def create_book(db: AsyncSession, book: schemas.BookCreate):
    db_book = models.Book(**book.model_dump())
    db.add(db_book)
    await db.commit()
    await db.refresh(db_book)
    return db_book

async def read_books(db: AsyncSession):
    result = await db.execute(select(models.Book))
    return result.scalars().all()

async def delete_book(db: AsyncSession, book_id: int):
    book = await db.get(models.Book, book_id)
    if book:
        await db.delete(book)
        await db.commit()
    return book