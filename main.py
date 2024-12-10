from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from models import SessionLocal, BookDB
from schemas import BookCreate, Book

app = FastAPI()

@app.get("/")
def read_root():
    return{"message":"Hello!"}

# Connect to the database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
# Create a book
@app.post("/books/", response_model=Book)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    new_book_db = BookDB(title=book.title, author=book.author, description=book.description)
    db.add(new_book_db)
    db.commit()
    db.refresh(new_book_db)
    return new_book_db

# Read all books
@app.get("/books/", response_model=list[Book])
def get_books(db: Session = Depends(get_db)):
    books_db = db.query(BookDB).all()
    return books_db

# Read one book
@app.get("/books/{book_id}", response_model=Book)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book_db = db.query(BookDB).filter(BookDB.id == book_id).first()
    if not book_db:
        raise HTTPException(status_code=404, detail="Book not found")
    return book_db

#Update a book
@app.put("/books/{book_id}", response_model=Book)
def update_book(book_id: int, book: BookCreate, db: Session = Depends(get_db)):
    db_book = db.query(BookDB).filter(BookDB.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    db_book.title = book.title
    db_book.author = book.author
    db_book.description = book.description
    
    db.commit()
    db.refresh(db_book)
    return db_book

# Delete a book
@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    db_book = db.query(BookDB).filter(BookDB.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(db_book)
    db.commit()
    return {"message": "Book deleted successfully"}