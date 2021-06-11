from flask import Flask, request, render_template
import json 
import os
import requests

import sys
sys.path.append(os.path.abspath(os.path.join(__file__, '..', '..')))
import configuration

app = Flask(__name__)

def query_backend(request, endpoint, params):
    base_domain = request.base_url.rsplit(':', 1)[0]
    backend_url = f'{base_domain}:{str(configuration.backend_port)}/'
    return requests.get(url=f'{backend_url}{endpoint}', headers=configuration.headers, params=params)

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
            search_results = query_backend(request, 'search', params={'searchquery': data['searchquery']}).json()
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
    base_domain = request.base_url.rsplit(':', 1)[0]
    backend_url = f'{base_domain}:{str(configuration.backend_port)}/'
    return render_template(
        'book.html',
        book = query_backend(request, 'book', params={'url': bookurl}).json(),
        download_endpoint = backend_url + 'download',
        quote = requests.utils.quote
    )

@app.route('/book', methods=['POST'])
def downloadBook():
    response = query_backend(request, 'download', params= {
        'url': request.values.get('url'),
        'title': request.values.get('title'),
        'authors': request.values.get('authors'),
        'description': request.values.get('description'),
        'thumbnail': request.values.get('thumbnail')
    })
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

@app.route('/read', methods=['GET'])
def getBooks():
    response = query_backend(request, 'getallbooks', params=None).json()
    books = json.loads(response)
    return render_template(
        'all_books.html',
        books = books
    )

@app.route('/read/<book_id>', methods=['GET'])
def readBook(book_id):
    response = query_backend(request, 'read/' + book_id, params=None).json()
    return render_template(
        'readbook.html',
        book = response
    )

def get_chapter_name(chapter_url):
    chapter = chapter_url.rsplit('/', 1)[1]
    return f'Chapter {str(int(chapter) + 1)}'

@app.route('/read/<book_id>/<chapter_id>', methods=['GET'])
def readChatper(book_id, chapter_id):
    response = query_backend(request, f'read/{book_id}/{chapter_id}', params=None).json()
    return render_template(
        'readchapter.html',
        chapter_info = response,
        chapter_to_text = get_chapter_name
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=configuration.frontend_port, debug=True)
