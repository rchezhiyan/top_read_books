"""CRUD operation"""

from model import db, User, Book, Author, BookAuthor, UserBooks, connect_to_db
from sqlalchemy import func, desc, select, cast, Numeric, Integer

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

def get_user_by_email(email):
    """Return a user by email."""

    return User.query.filter(User.email == email).first()


def get_books():
    """Return all books."""

    return Book.query.limit(30).all()

def get_book_by_id(book_id):
    """Return a movie by primary key."""

    return Book.query.get(book_id)

def get_book_by_isbn(isbn13):
    """Return a movie by primary key."""

    return Book.query.filter(Book.isbn13==isbn13).first()

def get_author_by_name(name):
    """Return a movie by primary key."""

    return Author.query.filter(Author.name==name).first()

def get_top_books():
    """Return the top 10 books"""
    # Query used:
    # SELECT title, RANK() OVER(ORDER BY gr_avg_rating DESC, num_of_ratings DESC, num_of_reviews DESC) as RANK
    # FROM books
    # LIMIT 10;

    top_books = db.session.query(
    Book,
    func.rank().over(
        order_by=(Book.gr_avg_rating.desc(), Book.num_of_ratings.desc())
    ).label('book_rank')).limit(10).all()

    return top_books

def get_user_favbks(user_id):

    # SELECT fav_book_id
    # FROM user_books
    # WHERE user_id = user_id;

    user = get_user_by_id(user_id)

    return user.books

def authors_books_report():

    # Bar Chart:
    # SELECT a.name, count(*) as Books_count
    # FROM authors a
    # JOIN book_authors ba ON a.id = ba.author_id
    # GROUP BY 1
    # ORDER BY 2;

    # bubble chart report:
    # SELECT a.name, count(b.id), round(avg(gr_avg_rating),2) as avg_rating, round(avg(num_of_ratings),0) as avg_ratings
    # from books b
    # JOIN book_authors ba ON ba.book_id = b.id
    # JOIN authors a ON a.id = ba.author_id
    # GROUP BY 1;

    data = db.session.query(Author.name
                ,func.count(BookAuthor.book_id).label('bookcount')).join(BookAuthor).group_by('name').order_by(desc('bookcount')).limit(10).all()

    return data

def bubble_report():

    # stmt = select(User).join(User.orders).join(Order.items).join(User.addresses)

    data = db.session.query(Author.name
                ,func.count(BookAuthor.book_id).label('book_count')
                ,cast(func.round(func.avg(Book.gr_avg_rating),2), Numeric).label('avg_rating')
                ,cast(func.round(func.avg(Book.num_of_ratings),0), Integer).label('num_of_ratings')).join(BookAuthor, BookAuthor.author_id == Author.id).join(Book, Book.id == BookAuthor.book_id).group_by('name').order_by(desc('num_of_ratings')).all()
    

    return data

def to_dict(objlist):

    # {k: v for k, v in d.items() if k not in keys}
    output = {}
    index = 0
    for obj in objlist:

        output[f'book_{index}']= {k:item for k,item in obj.__dict__.items() 
                    if k not in ['_sa_instance_state', 'gr_avg_rating']}
        index += 1
    return output

def search_books_byname(keyword):

    # SELECT *
    # FROM books b
    # WHERE lower(b.title) like ('%keyword%');

    booklist = Book.query.filter(func.lower(Book.title).like(f'%{keyword}%')).all()

    return to_dict(booklist)




if __name__ == "__main__":
    from server import app

    connect_to_db(app)

