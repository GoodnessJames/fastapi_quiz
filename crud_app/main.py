from typing import List
from fastapi import FastAPI, status, HTTPException, Depends
from fastapi.openapi.utils import get_openapi
from database import Base, engine, SessionLocal
from sqlalchemy.orm import Session
import models
import schemas
import re

Base.metadata.create_all(engine)

app = FastAPI()

def get_session():
    """
    Dependency function to retrieve a database session.

    Yields:
        Session: SQLAlchemy database session.

    Returns:
        generator: Generator yielding a database session.
    """
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

def is_valid_isbn(isbn: str) -> bool:
    """
    Validates if the provided ISBN is in a correct format.

    Args:
        isbn (str): ISBN to validate.

    Returns:
        bool: True if the ISBN is valid, False otherwise.
    """
    isbn_pattern = r"^\d{3}-?\d{1,5}-?\d{1,7}-?\d{1,7}-?\d{1}$"
    return bool(re.match(isbn_pattern, isbn))

@app.get("/", tags=["Root"])
def root():
    """
    Root endpoint.

    Returns:
        str: A simple message.
    """
    return "Books"

@app.post("/books", response_model=schemas.Book, status_code=status.HTTP_201_CREATED, tags=["Books"])
def create_book(book: schemas.BookCreate, session: Session = Depends(get_session)):
    """
    Create a new book.

    Args:
        book (schemas.BookCreate): Data for the new book.
        session (Session, optional): Database session. Defaults to Depends(get_session).

    Returns:
        models.Book: Created book.
    """
    if not isinstance(book.title, str) or not isinstance(book.author, str) \
            or not isinstance(book.year, int) or not is_valid_isbn(book.isbn):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid input data")

    if book.year < 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid year")

    book_db = models.Book(**book.dict())
    session.add(book_db)
    session.commit()
    session.refresh(book_db)
    return book_db

@app.get("/books/{id}", response_model=schemas.Book, tags=["Books"])
def read_book(id: int, session: Session = Depends(get_session)):
    """
    Retrieve a book by ID.

    Args:
        id (int): Book ID.
        session (Session, optional): Database session. Defaults to Depends(get_session).

    Raises:
        HTTPException: If book not found.

    Returns:
        models.Book: Retrieved book.
    """
    book = session.query(models.Book).get(id)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with id {id} not found")
    return book

@app.put("/books/{id}", response_model=schemas.Book, tags=["Books"])
def update_book(id: int, book_data: schemas.BookUpdate, session: Session = Depends(get_session)):
    """
    Update a book by ID.

    Args:
        id (int): Book ID.
        book_data: Data for the book update.
        session (Session, optional): Database session. Defaults to Depends(get_session).

    Raises:
        HTTPException: If book not found.

    Returns:
        book: Retrieved book.
    """
    book = session.query(models.Book).get(id)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with id {id} not found")

    for field, value in book_data.dict(exclude_unset=True).items():
        setattr(book, field, value)
    session.commit()
    return book

@app.delete("/books/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Books"])
def delete_book(id: int, session: Session = Depends(get_session)):
    """
    Deletes a book by ID.

    Args:
        id (int): Book ID.
        session (Session, optional): Database session. Defaults to Depends(get_session).

    Raises:
        HTTPException: If book not found.
    """
    book = session.query(models.Book).get(id)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with id {id} not found")
    session.delete(book)
    session.commit()

@app.get("/books", response_model=List[schemas.Book], tags=["Books"])
def read_books(session: Session = Depends(get_session)):
    """
    Retrieve a list of books.

    Args:
        session (Session, optional): Database session. Defaults to Depends(get_session).

    Raises:
        HTTPException: If book not found.

    Returns:
        books: Retrieved books.
    """
    books = session.query(models.Book).all()
    return books

def custom_openapi():
    """
    Custom function to generate OpenAPI schema for the API documentation.

    Returns:
        dict: OpenAPI schema definition.
    """
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Book API",
        version="1.0.0",
        description="This is a simple CRUD API for managing a collection of books.",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
