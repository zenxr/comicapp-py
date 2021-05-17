from flask import Flask, request, render_template
import json
import os
import requests

import sys
sys.path.append(os.path.abspath(os.path.join(__file__, '..', '..')))
from configuration import headers

app = Flask(__name__)
BACKEND_URL = 'http://127.0.0.1:5000/'

def query_backend(endpoint, params):
    return requests.get(url=f'{BACKEND_URL}{endpoint}', headers=headers, params=params)

@app.route('/')
def index():
    return render_template(
        'index.html',
        search_results = []
)

@app.route('/', methods=['POST'])
def searchPost():
    try:
        data = request.form.to_dict()
        if data['searchquery']:
            search_results = query_backend('search', params={'searchquery': data['searchquery']}).json()
            search_results = json.loads(search_results)
        return render_template(
            'index.html',
            search_results = search_results
        )
    except:
        return render_template(
            'index.html',
            search_results = []
        )

@app.route('/book')
def getBook():
    bookurl = request.values.get('bookurl')
    return render_template(
        'book.html',
        book = query_backend('book', params={'url': bookurl}).json(),
        download_endpoint = BACKEND_URL + 'download',
        quote = requests.utils.quote
    )

@app.route('/book', methods=['POST'])
def downloadBook():
    bookurl = request.values.get('url')
    title = request.values.get('title')
    authors = request.values.get('authors')
    description = request.values.get('description')
    response = query_backend('download', params= {
        'url': bookurl,
        'title': title,
        'authors': authors,
        'description': description
    })
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

@app.route('/read', methods=['GET'])
def getBooks():
    response = query_backend('getallbooks', params=None).json()
    books = json.loads(response)
    return render_template(
        'all_books.html',
        books = books
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)