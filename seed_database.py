""""Script to seed the database"""

import os
import json
import csv

import crud
import model
import server

os.system("dropdb books")
os.system("createdb books")

model.connect_to_db(server.app)
model.db.create_all()

#Loading the sample book data:

with open("data/sample_data_books.csv") as f:
    reader = csv.DictReader(f)

    books_db = []

    for row in reader:
       title = row["title"]
       isbn13 = row["isbn13"]
       num_pages = int(row["num_pages"])
       gr_avg_rating = float(row["average_rating"])
       num_of_ratings = int(row["num_of_ratings"])
       num_of_reviews = int(row["num_of_reviews"])

       db_book = crud.create_book(title, isbn13, num_pages, gr_avg_rating, num_of_ratings, num_of_reviews, book_cover = None)
       books_db.append(db_book)

model.db.session.add_all(books_db)
model.db.session.commit() 

#Loading the book authors relationship data:

with open("data/book_authors.csv") as f:
    reader = csv.DictReader(f)

    authors_db = []
    authors_check = []

    for row in reader:
        name = row["authors"]

        if name not in authors_check:
            authors_check.append(name)
            db_author = crud.create_author(name=name)
            authors_db.append(db_author)
        else:
            pass

model.db.session.add_all(authors_db)
model.db.session.commit()

with open("data/book_authors.csv") as f:
    reader = csv.DictReader(f)

    for row in reader:
        name = row["authors"]
        isbn13 = row["isbn13"]

        bk = crud.get_book_by_isbn(isbn13)

        authr = crud.get_author_by_name(name)

        bk.authors.append(authr)
        authr.books.append(bk)

        model.db.session.commit()

