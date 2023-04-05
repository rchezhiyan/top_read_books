"""Model for the top read books app"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# books

class Book(db.Model):
    """A Book"""

    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=True)
    isbn13 = db.Column(db.String(17), unique=True)
    num_pages = db.Column(db.Integer, nullable=True)
    book_cover = db.Column(db.String)
    gr_avg_rating = db.Column(db.Numeric(3,2))
    num_of_ratings = db.Column(db.Integer)
    num_of_reviews = db.Column(db.Integer)

    authors = db.relationship("Author", secondary="book_authors", back_populates="books")
    users = db.relationship("User", secondary="user_books", back_populates="books")

    def __repr__(self):
        return f"<Book book_id={self.id} title={self.title}>"

# authors
class Author(db.Model):
    """An author"""

    __tablename__ = "authors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    auth_wiki = db.Column(db.String)

    books = db.relationship("Book", secondary="book_authors", back_populates="authors")

    def __repr__(self):
        return f"<Author author_id={self.id} author_name={self.name}>"

class BookAuthor(db.Model):
    """ Book author relations table"""

    __tablename__ = "book_authors"

    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("authors.id"), nullable=False)

# users
class User(db.Model):
    """A User."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30))
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)

    books = db.relationship("Book", secondary="user_books", back_populates="users")

    def __repr__(self):
        return f"<User user_id={self.id} username={self.username} email={self.email}>"

class UserBooks(db.Model):
    """Users Favourite books table object"""

    __tablename__ = "user_books"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    fav_book_id = db.Column(db.Integer, db.ForeignKey("books.id"))


def connect_to_db(flask_app, db_uri="postgresql:///books", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")

if __name__ == "__main__":
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)


