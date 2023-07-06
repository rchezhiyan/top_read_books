"""Server for top book to read app"""

from flask import Flask, render_template, request, flash, session, redirect, jsonify
from model import connect_to_db, db
import crud
import google_book
import json

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

    user_id = session.get("user_id",None)
    if user_id:
        fav_books = crud.get_user_favbks(user_id)
    else:
        fav_books = []

    gdata = google_book.google_book_data(book.isbn13)

    if gdata is None:
        data = None
    else:
        data = gdata["items"][0]["volumeInfo"].get('description')

    return render_template("book_details.html", book=book, favbooks=fav_books,
                            data=data)

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

    email = request.json.get("email")
    password = request.json.get("pwd")

    print(f"EMAIL: {email} PASSWORD: {password}")

    user = crud.get_user_by_email(email)
    if not user or user.password != password:
        flash("The email or password you entered was incorrect.")
        msg="error"
    else:
        # Log in user by storing the user's email in session
        session["username"] = user.username
        session["user_id"] = user.id
        flash(f"Welcome back, {user.username}!")
        msg = 'Success'

    return msg

@app.route("/login")
def show_login():

    return render_template('login.html')

@app.route("/logout")
def handle_logout():

    session.clear()


    return redirect('/')


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

    user_id = session.get("user_id",None)

    if user_id is None:

        flash(f"Please login to see the favorite books!")

        return redirect("/login")

    fav_books = crud.get_user_favbks(user_id)

    return render_template("fav_books.html", books=fav_books)

@app.route("/bar_chart")
def show_chart():

    return render_template("bar_chart.html")

@app.route('/author_books.json')
def get_report_data():

    data = crud.authors_books_report()

    result = [{k: item[k] for k in item.keys()} for item in data]
    print (result)
    print(jsonify(result))
    return jsonify(result)

@app.route("/bubble_chart")
def show_bubble_chart():

    return render_template("bubble_chart.html")

@app.route("/bubble_data.json")
def get_bubble_data():
    
    data = crud.bubble_report()
    # result = [{k: item[k] for k in item.keys()} for item in data]

    result = []
    for item in data: 
        res = {}
        for k in item.keys():
            if k == 'avg_rating':
                res[k] = float(item[k])
            else:
                res[k] = item[k]
        result.append(res)

    return jsonify(result)



@app.route('/search')
def show_search():

    return render_template("search.html")

@app.route('/search.json', methods=["POST"])
def process_search():

    keyword = request.json.get("searchtxt")

    booklist = crud.search_books_byname(keyword)

    return json.dumps(booklist)

    

if __name__ == "__main__":

    connect_to_db(app)

    app.run(host="0.0.0.0", debug=True, port=5001)