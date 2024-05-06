from sqlalchemy import Column, Integer, String
from database import Base


class Book(Base):
    """
    Represents a book in the database.

    Attributes:
        id (int): The unique identifier for the book.
        title (str): The title of the book.
        author (str): The author of the book.
        year (int): The year of publication of the book.
        isbn (str): The ISBN (International Standard Book Number) of the book.
    """
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    author = Column(String)
    year = Column(Integer)
    isbn = Column(String)
