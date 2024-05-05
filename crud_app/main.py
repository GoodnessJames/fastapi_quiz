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
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

def is_valid_isbn(isbn: str) -> bool:
    isbn_pattern = r"^\d{3}-?\d{1,5}-?\d{1,7}-?\d{1,7}-?\d{1}$"
    return bool(re.match(isbn_pattern, isbn))

@app.get("/", tags=["Root"])
def root():
    return "Books"

@app.post("/books", response_model=schemas.Book, status_code=status.HTTP_201_CREATED, tags=["Books"])
def create_book(book: schemas.BookCreate, session: Session = Depends(get_session)):
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
    book = session.query(models.Book).get(id)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with id {id} not found")
    return book

@app.put("/books/{id}", response_model=schemas.Book, tags=["Books"])
def update_book(id: int, book_data: schemas.BookUpdate, session: Session = Depends(get_session)):
    book = session.query(models.Book).get(id)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with id {id} not found")

    for field, value in book_data.dict(exclude_unset=True).items():
        setattr(book, field, value)
    session.commit()
    return book

@app.delete("/books/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Books"])
def delete_book(id: int, session: Session = Depends(get_session)):
    book = session.query(models.Book).get(id)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with id {id} not found")
    session.delete(book)
    session.commit()

@app.get("/books", response_model=List[schemas.Book], tags=["Books"])
def read_books(session: Session = Depends(get_session)):
    books = session.query(models.Book).all()
    return books

# This part adds OpenAPI documentation to the endpoints
def custom_openapi():
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