from flask import Flask, render_template, request
from pprint import pformat
import os
import requests
import server


API_KEY = os.environ['BOOKAPI_KEY']

def google_book_data(isbn13):
    """Access and fetch data from google api"""

    url = f'https://www.googleapis.com/books/v1/volumes?q=+isbn:{isbn13}&key={API_KEY}'

    print(url)
    res = requests.get(url)
    data = res.json()

    print(data)

    if data["totalItems"] == 0:
        return None

    # Book Description:
    # data["items"][0]["volumeInfo"]["description"]
    #Book Id for google query:
    # gdata['items'][0]['id']

    return data
