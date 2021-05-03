from flask import Flask

from ComicSearch.mangakalot_search import MangakalotSearch
from ComicSearch.mangakalot_book import MangakalotBook
from ComicSearch.search import BasicSearchQuery

def main():
    query = BasicSearchQuery('solo_leveling')
    response = MangakalotSearch().search(query)
    return response

def page():
    url = 'https://manganelo.com/manga/pn918005'
    return MangakalotBook(url).fetch()

if __name__ == '__main__':
    main()


# app = Flask(__name__)

# @app.route("/")
# def hello():
#     return "Hello world"

# if __name__ == "__main__":
#     app.run()