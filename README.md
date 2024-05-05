# FastAPI CRUD Application
A simple CRUD (Create, Read, Update, Delete) application built with FastAPI and SQLAlchemy that allows managing a collection of books in a database.

## Requirements
Python 3.7+

Pip (Python package manager)

## Installation
1. Clone the repository:
```
git clone https://github.com/GoodnessJames/fastapi.git
```
2. Navigate to the project directory:
```
cd fastapi/crud_app
```
3. Install dependencies:
```
pip install -r requirements.txt
```
## Running the Application
1. Run the FastAPI application using uvicorn:
```
uvicorn main:app --reload
```

- The --reload flag enables automatic reloading of the server when changes are made to the code.

2. Access the API documentation: Open your web browser and navigate to http://127.0.0.1:8000/docs. You should see the Swagger documentation for your FastAPI application, where you can interact with the API endpoints and test their functionality.

## API Endpoints
GET /books: Retrieve a list of all books.

GET /books/{id}: Retrieve information about a specific book.

POST /books: Add a new book to the collection.

PUT /books/{id}: Update information about a specific book.

DELETE /books/{id}: Delete a book from the collection.

## Input Validation
- Required fields: title, author, year, isbn.
- Validate input types and formats: year should be an integer, isbn should be a string.
- ISBN numbers should be hyphen-separated.

## Custom Validation
ISBN validation allows for hyphen-separated numbers.

## Dependencies
FastAPI: Web framework for building APIs with Python 3.7+.

SQLAlchemy: SQL toolkit and Object-Relational Mapping (ORM) library for Python.

Pydantic: Data validation and settings management using Python type annotations.

uvicorn: ASGI server for running FastAPI applications.

## Contributions
Feel free to open an issue or submit a pull request.
