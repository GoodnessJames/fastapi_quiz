from pydantic import BaseModel, Field
from typing import Optional

 
class BookCreate(BaseModel):
    """
    Schema for creating a new book.

    Attributes:
        title (str): The title of the book.
        author (str): The author of the book.
        year (int): The year of publication of the book.
        isbn (str): The ISBN (International Standard Book Number) of the book.
    """
    title: str
    author: str
    year: int
    isbn: str
 

class Book(BaseModel):
    """
    Schema representing a book.

    Attributes:
        id (int): The unique identifier for the book.
        title (str): The title of the book.
        author (str): The author of the book.
        year (int): The year of publication of the book.
        isbn (str): The ISBN (International Standard Book Number) of the book.
    """
    id: int
    title: str
    author: str
    year: int
    isbn: str


class BookUpdate(BaseModel):
    """
    Schema for updating book information.

    Attributes:
        title (Optional[str]): The updated title of the book.
        author (Optional[str]): The updated author of the book.
        year (Optional[int]): The updated year of publication of the book.
        isbn (Optional[str]): The updated ISBN (International Standard Book Number) of the book.

    Config:
        orm_mode (bool): Allows to use this Pydantic model with ORM.
    """
    title: Optional[str] = Field(None, title="Title of the book")
    author: Optional[str] = Field(None, title="Author of the book")
    year: Optional[int] = Field(None, title="Year of publication")
    isbn: Optional[str] = Field(None, title="ISBN of the book")
 
    class Config:
        orm_mode = True
