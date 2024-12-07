from pydantic import BaseModel
from typing import Optional

# Base schema: What information a book has
class BookBase(BaseModel):
    title: str
    author: str
    description: str
    
# Schema for creating a new book
class BookCreate(BookBase):
    pass

# Schema for reading a book (includes ID)
class Book(BookBase):
    id: int
    
    class Config:
        orm_mode = True # Helps convert database objects to schemas