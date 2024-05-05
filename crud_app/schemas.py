from pydantic import BaseModel, Field
from typing import Optional

 
class BookCreate(BaseModel):
    title: str
    author: str
    year: int
    isbn: str
 
# Complete Book Schema (Pydantic Model)
class Book(BaseModel):
    id: int
    title: str
    author: str
    year: int
    isbn: str

# Pydantic model for updating a book
class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, title="Title of the book")
    author: Optional[str] = Field(None, title="Author of the book")
    year: Optional[int] = Field(None, title="Year of publication")
    isbn: Optional[str] = Field(None, title="ISBN of the book")
 
    class Config:
        orm_mode = True