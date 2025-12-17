# app_book_author/schema.py
from pydantic import BaseModel, field_validator
from datetime import datetime


class AuthorCreate(BaseModel):
    name: str

class AuthorRead(AuthorCreate):
    id: int

    class Config:
        # orm_mode = True
        from_attributes = True

    @field_validator("name")
    @classmethod
    def name_valid(cls, v):
        return v.upper()

class BookCreate(BaseModel):
    title: str
    published_year: int
    author_id : int


    @field_validator('published_year')
    @classmethod
    def year_valid(cls, v:int) -> int:
        if v >= datetime.now().year:
            raise ValueError("Published year should not be in the future")
        return v

class BookRead(BookCreate):
    id: int
    author: AuthorRead

    class Config:
        # orm_mode = True
        from_attributes = True

    @field_validator('title')
    @classmethod
    def title_valid(cls, v:str) -> str:
        return f"Book: {v}"
