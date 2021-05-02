from flask import Flask

from ComicSearch.mangakalot_search import MangakalotSearch
from ComicSearch.search import BasicSearchQuery


if __name__ == '__main__':
    query = BasicSearchQuery('solo_leveling')
    response = MangakalotSearch().search(query)

# app = Flask(__name__)

# @app.route("/")
# def hello():
#     return "Hello world"

# if __name__ == "__main__":
#     app.run()