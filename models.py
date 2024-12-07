from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#Create a database connection
DATABASE_URL = "sqlite:///./test.db" # SQLite makes a file called `test.db`
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

#Setup database classes
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

#Define a book for database
class BookDB(Base):
    __tablename__ = 'books'
    
    id = Column(Integer, primary_key=True, index=True) # Unique ID
    title = Column(String, index=True)  # Book title
    author = Column(String)             # Book author
    description = Column(String)        # Book description  
    
# Create the "books" table   
Base.metadata.create_all(bind=engine)