# app_book_author/crud.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, delete, update, func
from . import models, schemas
from collections import defaultdict
from sqlalchemy.orm import joinedload


# commit()      ذخیره دستور
# cursor()      اجرای دستور
# execute(select(models.Book).where(models.Book.author_id == 1))     ارسال دستور
# fetchall()    دریافت دستور بدون اسم ستون  tuple - وقتی چند ستون خاص را می‌خواهی
# scalars().all()     دریافت دستور با اسم ستون  dict - وقتی کل یک مدل را با تمام ستون‌هایش می‌خواهی
# برای لیست‌ها: ()scalars().all
# برای تکی‌ها: ()scalars().first
# rowcount  برای خذف


# --- Authors ---
async def create_author(db: AsyncSession, author: schemas.AuthorCreate):
    # db_author = models.Author(**author.model_dump())
    # db.add(db_author)
    # await db.commit()
    # await db.refresh(db_author)
    # return db_author

    result = await db.execute(insert(models.Author)
                              .values(**author.model_dump())
                              .returning(models.Author))
    await db.commit()
    return result.scalars().first()

async def read_authors(db: AsyncSession):
    result = await db.execute(select(models.Author))
    return result.scalars().all()

async def read_author(db: AsyncSession, author_id: int):
    result = await db.execute(select(models.Author).where(models.Author.id == author_id))
    return result.scalars().first()

async def update_author_name(db: AsyncSession, author_id: int, new_name: str):
    # author = await db.get(models.Author, author_id)
    # if author:
    #     author.name = new_name
    #     await db.commit()
    #     await db.refresh(author)
    # return author

    result = await db.execute(update(models.Author).where(models.Author.id == author_id)
                              .values(name=new_name)
                              .returning(models.Author))
    await db.commit()
    return result.scalars().first()

# --- Books ---
async def create_book(db: AsyncSession, book: schemas.BookCreate):
    # db_book = models.Book(**book.model_dump())
    # db.add(db_book)
    # await db.commit()
    # await db.refresh(db_book)
    # return db_book

    result = await db.execute(insert(models.Book)
                              .values(**book.model_dump())  # 👈 تبدیل شِمای پایدنتیک به دیکشنری برای دیتابیس
                              .returning(models.Book))   # 👈 بازگرداندن سطر ساخته شده (شامل ID که دیتابیس ساخته)
    await db.commit()
    return result.scalars().first()

async def read_books(db: AsyncSession):
    # حتماً نویسنده را JOIN کن تا Pydantic خطا ندهد
    result = await db.execute(select(models.Book)).options(joinedload(models.Book.author))
    return result.scalars().all()

async def read_book(db: AsyncSession, book_id: int):
    # حتماً نویسنده را JOIN کن تا Pydantic خطا ندهد
    result = await db.execute(select(models.Book).where(models.Book.id == book_id).options(joinedload(models.Book.author)))
    return result.scalars().first()

async def delete_book(db: AsyncSession, book_id: int):
    # book = await db.get(models.Book, book_id)
    # if book:
    #     await db.delete(book)
    #     await db.commit()
    # return book

    result = await db.execute(delete(models.Book).where(models.Book.id == book_id))
    await db.commit()
    return result.rowcount

async def get_fast_author_stats(db: AsyncSession):
    # این کوئری روی 500 req/s جوابه
    result = await db.execute(text("SELECT author_name, book_count FROM author_book_counts"))
    return [{"author": row[0], "count": row[1]} for row in result.fetchall()]

async def get_books_count_by_author(db: AsyncSession):
    # result = await db.execute(select(models.Book))
    # all_books = result.scalars().all()
    # lst_books = defaultdict(list)
    # for book in all_books:
    #     lst_books[book.author_id].append(book)
    # return lst_books

                    # ۱. چی می‌خوایم؟ نام نویسنده و "تعدادآیدی کتاب‌ها" (, func---> avg,sum,concat,min,max,count)
    result = await db.execute(select(models.Author.name, func.count(models.Book.id).label('book_count'))
                              .join(models.Book)            # ۲. چطوری بهم وصل بشن؟ از روی رابطه آیدی نویسنده در جدول کتاب
                              .group_by(models.Author.id))   # ۳. چطوری دسته‌بندی بشن؟ کتاب‌ها رو بر اساس آیدی نویسنده بذار توی "پوشه‌های" جداگانه
    return [{"author": i[0], "count": i[1]} for i in result.fetchall()]

async def get_books_by_author_id(db: AsyncSession, author_id: int):
    result = await db.execute(select(models.Book).where(models.Book.author_id == author_id).options(joinedload(models.Book.author)))
    return result.scalars().all()

async def get_books_yearly(db: AsyncSession):
    result = await db.execute(select(models.Book.published_year, func.count(models.Book.id).label('book_count'))
                              .group_by(models.Book.published_year))
    return result.fetchall()

async def get_books_yearly_by_author(db: AsyncSession):
    result = await db.execute(select(models.Author.name, models.Book.published_year, func.count(models.Book.id).label('book_count'))
                              .join(models.Book)
                              .group_by(models.Author.id ,models.Book.published_year))
    return result.fetchall()
