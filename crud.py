"""CRUD operation"""

from model import db, User, Book, Author, BookAuthor, UserBooks, connect_to_db

def create_user(email, username, password):
    """Create and return a user."""

    user = User(email=email, username=username, password=password)

    return user

def create_author(name):
    """Create and return a user."""

    author = Author(name=name)

    return author

def create_book(title, isbn13, num_pages, gr_avg_rating, num_of_ratings, num_of_reviews, book_cover = None,):
    """Create and return a book."""

    book = Book(
        title=title,
        isbn13=isbn13,
        num_pages=num_pages,
        book_cover=book_cover,
        gr_avg_rating=gr_avg_rating,
        num_of_ratings=num_of_ratings,
        num_of_reviews=num_of_reviews,
    )

    return book

def get_user_by_id(user_id):
    """Return a user by primary key."""

    return User.query.get(user_id)

def get_users():
    """Return all users."""

    return User.query.all()

def get_books():
    """Return all books."""

    return Book.query.all()

def get_book_by_id(book_id):
    """Return a movie by primary key."""

    return Book.query.get(book_id)

def get_book_by_isbn(isbn13):
    """Return a movie by primary key."""

    return Book.query.filter(Book.isbn13==isbn13).first()

def get_author_by_name(name):
    """Return a movie by primary key."""

    return Author.query.filter(Author.name==name).first()

if __name__ == "__main__":
    from server import app

    connect_to_db(app)

