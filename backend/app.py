from flask import Flask, request, Response, send_from_directory
from requests.models import ContentDecodingError
from flask_restful import reqparse, Api, Resource
from requests.utils import unquote
import json
import os
import sys

sys.path.append(os.path.abspath(os.path.join(__file__, '..', '..')))
import configuration
from ComicSearch.mangakalot_book import MangakalotBook
from ComicSearch.mangakalot_search import MangakalotSearch
from ComicSearch.search import BasicSearchQuery
from ComicDownloader.downloader import download, getSeriesMutliProc, getSeries

app = Flask(__name__)
api = Api(app)
app_url = "http://127.0.0.1:5000"

def get_parser(*args):
    parser = reqparse.RequestParser()
    for arg in args:
        parser.add_argument(arg)
    return parser

def saveseriesmetadata(url, title, authors, description, thumbnail):
    name = url.rsplit('/', 1)[1]
    if '.' in name:
        name = name.split('.', 1)[0]
    output_filename = name + '.json'
    if not os.path.exists(configuration.download_dir):
        os.mkdir(configuration.download_dir)
    metadata = {
        'url': url,
        'title': title,
        'authors': authors,
        'description': description,
        'id': name,
        'thumbnail': thumbnail
    }
    with open(output_filename, 'w') as f:
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
        # getSeriesMutliProc(args.url, configuration.download_dir)
        getSeries(args.url, configuration.download_dir)
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

@app.route('/read/<book_id>')
def getBook(book_id):
    comic_dir = configuration.download_dir
    with open(os.path.join(comic_dir, book_id + '.json'), 'r') as f:
        info = json.loads(f.read())
    chapter_path = os.path.join(comic_dir, book_id)
    chapters = os.listdir(chapter_path)
    chapter_dict = {}
    chapters.sort()
    for chapter in chapters:
        chapter_dict[chapter] = f'./{book_id}/{chapter}'
    info['chapters'] = chapter_dict
    return json.dumps(info)

@app.route('/read/<book_id>/<chapter_id>')
def getChapter(book_id, chapter_id):
    response = {}
    response['current_chapter'] = f'/read/{book_id}/{chapter_id}'
    # response['current_chapter'] = str(int(chapter_id) + 1)
    chapters = os.listdir(os.path.join(configuration.download_dir, book_id))
    response['chapters'] = [f'/read/{book_id}/{c}' for c in chapters]
    response['chapters'].sort()
    with open(os.path.join(configuration.download_dir, book_id + '.json'), 'r') as f:
        book_info = json.loads(f.read())
    response['title'] = book_info['title']
    base_path = request.base_url.rsplit('/', 3)[0]
    chapter_dir = f'{configuration.download_dir}/{book_id}/{chapter_id}'
    pages = os.listdir(chapter_dir)
    pages.sort()
    response['pages'] = [f'{base_path}/comics/{book_id}/{chapter_id}/{p}' for p in pages]
    return json.dumps(response)

@app.route('/comics/<path:path>')
def send_file(path):
    return send_from_directory(configuration.download_dir, path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=configuration.port, debug=True)
