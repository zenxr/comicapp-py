from flask import Flask, request, Response
from requests.models import ContentDecodingError
from flask_restful import reqparse, Api, Resource
from requests.utils import unquote

import json

from ComicSearch.mangakalot_book import MangakalotBook
from ComicSearch.mangakalot_search import MangakalotSearch
from ComicSearch.search import BasicSearchQuery
from ComicDownloader.downloader import download, getSeriesMutliProc
import configuration
import os

app = Flask(__name__)
api = Api(app)

def get_parser(*args):
    parser = reqparse.RequestParser()
    for arg in args:
        parser.add_argument(arg)
    return parser

def saveseriesmetadata(url, title, authors, description, thumbnail):
    output_filename = url.rsplit('/', 1)[1]
    if '.' in output_filename:
        output_filename = output_filename.split('.', 1)[0]
    output_filename = output_filename + '.json'
    if not os.path.exists(configuration.download_dir):
        os.mkdir(configuration.download_dir)
    outputfile = os.path.join(configuration.download_dir, output_filename)
    metadata = {
        'url': url,
        'title': title,
        'authors': authors,
        'description': description,
        'location': outputfile,
        'thumbnail': thumbnail
    }
    with open(outputfile, 'w') as f:
        json.dump(metadata, f, indent=4)

def get_file_json_contents(filepath):
    with open(filepath, 'r') as f:
        contents = json.load(f)
    return contents

class Search(Resource):
    def get(self):
        parser = get_parser('searchquery')
        args = parser.parse_args()
        query = BasicSearchQuery(args.searchquery.split())
        search_results = MangakalotSearch().search(query)
        return search_results

class Book(Resource):
    def get(self):
        parser = get_parser('url')
        args = parser.parse_args()
        return MangakalotBook(args.url).fetch()

class Download(Resource):
    def get(self):
        parser = get_parser('url', 'title', 'authors', 'description', 'thumbnail')
        args = parser.parse_args()
        args.url = unquote(args.url)
        args.title = unquote(args.title)
        args.authors = unquote(args.authors)
        args.description = unquote(args.description)
        args.thumbnail = unquote(args.thumbnail)
        saveseriesmetadata(args.url, args.title, args.authors, args.description, args.thumbnail)
        getSeriesMutliProc(args.url, configuration.download_dir)
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

class GetAllBooks(Resource):
    def get(self):
        download_dir_files = os.listdir(configuration.download_dir)
        download_dir_files = [os.path.join(configuration.download_dir, f) for f in download_dir_files if f.endswith('.json')]
        comic_meta_files = [f for f in download_dir_files if os.path.isfile(f)]
        return json.dumps([get_file_json_contents(f) for f in comic_meta_files])

api.add_resource(Search, '/search')
api.add_resource(Book, '/book')
api.add_resource(Download, '/download')
api.add_resource(GetAllBooks, '/getallbooks')

# TODO FINISH THIS
@app.route('/read/<book_id>')
def getBook():
    bookurl = request.values.get('bookurl')
    return render_template(
        'book.html',
        book = query_backend('book', params={'url': bookurl}).json(),
        download_endpoint = BACKEND_URL + 'download',
        quote = requests.utils.quote
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)