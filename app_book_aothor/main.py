# app_book_author/main.py
from fastapi import FastAPI, Depends, HTTPException
from app_book_author import models, dbs, schemas, crud
from sqlalchemy.ext.asyncio import AsyncSession
import redis.asyncio as redis
from app_book_author.utils.decorators import cached_resilient
from app_book_author.utils.middleware import PerformanceMiddleware

app = FastAPI(title="Bookstore API")
app.add_middleware(PerformanceMiddleware)

redis_client = redis.from_url("redis://localhost", decode_responses=True)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_db():
    async with dbs.AsyncSessionLocal() as session:
        yield session

@app.post("/authors/", response_model=schemas.AuthorRead)
async def create_author(author: schemas.AuthorCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_author(db=db, author=author)

@app.get("/authors/", response_model= list[schemas.AuthorRead])
async def read_authors(db: AsyncSession = Depends(get_db)):
    return await crud.read_authors(db=db)

@app.post("/books/", response_model=schemas.BookRead)
async def create_book(book: schemas.BookCreate, db: AsyncSession = Depends(get_db)):
    # ۱. ابتدا چک کن نویسنده وجود دارد یا نه
    author = await db.get(models.Author, book.author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    # ۲. حالا کتاب را بساز
    db_book = await crud.create_book(db=db, book=book)

    # ۳. کش را پاک کن (چون دیتای جدید اضافه شده)
    await redis_client.delete("read_books:():{}")  # کلید داینامیک دکوراتور
    return db_book

@app.get("/books/", response_model=list[schemas.BookRead])
@cached_resilient(expire_seconds=120)
async def read_books(db:AsyncSession = Depends(get_db)):
    return await crud.read_books(db=db)

@app.get("/books/{book_id}", response_model=schemas.BookRead)
async def read_book(book_id:int, db:AsyncSession = Depends(get_db)):
    book = await db.get(models.Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="book not found")
    return book