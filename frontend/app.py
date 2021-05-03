from flask import Flask, request, render_template
import json
import os

import sys
sys.path.append(os.path.abspath(os.path.join(__file__, '..', '..')))

from ComicSearch.mangakalot_book import MangakalotBook
from ComicSearch.mangakalot_search import MangakalotSearch
from ComicSearch.search import BasicSearchQuery

app = Flask(__name__)

@app.route('/')
def index():
    return render_template(
        'index.html',
        search_results = []
)

@app.route('/', methods=['POST'])
def searchPost():
    data = request.form.to_dict()
    if data['searchQuery']:
        query = BasicSearchQuery(data['searchQuery'].split())
        search_results = MangakalotSearch().search(query)
    return render_template(
        'index.html',
        search_results = [json.loads(sr) for sr in search_results]
    )

@app.route('/book')
def getBook():
    bookurl = request.values.get('bookurl')
    book_info = MangakalotBook(bookurl).fetch()
    return render_template(
        'book.html',
        book = book_info
    )