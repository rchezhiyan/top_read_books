"""Server for top book to read app"""

from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db, db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

@app.route("/")
def homepage():
    """View homepage"""

    return render_template("homepage.html")

@app.route("/books")
def all_books():
    """View All time top read books"""

    books = crud.get_books()

    return render_template("all_books.html", books=books)

@app.route("/books/<book_id>")
def show_book(book_id):

    book = crud.get_book_by_id(book_id)

    user_id = session["user_id"]
    fav_books = crud.get_user_favbks(user_id)

    return render_template("book_details.html", book=book, favbooks=fav_books)

@app.route("/top_books")
def top_books():

    top_books = crud.get_top_books()

    return render_template("top_book_details.html", books=top_books)

@app.route("/users", methods=["POST"])
def register_user():
    """Create a new user."""

    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")

    usr = crud.get_user_by_email(email)

    if usr:
        flash("Unable to create an account with the given email.Try Again!")

    else:
        usr = crud.create_user(email,username,password)
        db.session.add(usr)
        db.session.commit()
        flash("Account created sucessfully! Please log in.")

    return redirect("/")

@app.route("/login", methods=["POST"])
def process_login():
    """Process user login."""

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    if not user or user.password != password:
        flash("The email or password you entered was incorrect.")
    else:
        # Log in user by storing the user's email in session
        session["username"] = user.username
        session["user_id"] = user.id
        flash(f"Welcome back, {user.username}!")

    return redirect("/")

@app.route("/add_book")
def add_book():

    book_id = request.args.get("book_id")

    book = crud.get_book_by_id(book_id)

    user = crud.get_user_by_id(session["user_id"])

    user_books = user.books

    if book in user_books:
        msg = "Book already in your favorites"
    else:
        user.books.append(book)
        db.session.commit()
        msg = "Success"

    return msg

@app.route("/remove_book")
def remove_book():

    book_id = request.args.get("book_id")

    book = crud.get_book_by_id(book_id)

    user = crud.get_user_by_id(session["user_id"])

    user_books = user.books

    
    user.books.remove(book)
    db.session.commit()
    msg = "Success"

    return msg

@app.route("/fav_books")
def show_user_books():

    user_id = session["user_id"]
    fav_books = crud.get_user_favbks(user_id)

    return render_template("fav_books.html", books=fav_books)

@app.route("/bar_chart")
def show_chart():

    return render_template("bar_chart.html")

    

if __name__ == "__main__":

    connect_to_db(app)

    app.run(host="0.0.0.0", debug=True)