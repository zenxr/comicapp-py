from flask import Flask, request
from flask_restful import reqparse, Api, Resource

import json

from ComicSearch.mangakalot_book import MangakalotBook
from ComicSearch.mangakalot_search import MangakalotSearch
from ComicSearch.search import BasicSearchQuery
from ComicDownloader.downloader import getSeries
import configuration

app = Flask(__name__)
api = Api(app)

def get_parser(*args):
    parser = reqparse.RequestParser()
    for arg in args:
        parser.add_argument(arg)
    return parser

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
        parser = get_parser('url')
        args = parser.parse_args()
        getSeries()


api.add_resource(Search, '/search')
api.add_resource(Book, '/book')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)