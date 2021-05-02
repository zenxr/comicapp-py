import requests
from bs4 import BeautifulSoup

from ComicSearch.search import ComicSearch, ComicSearchConfig, BasicSearchQuery
from configuration import headers

class MangakalotSearch(ComicSearch):
    def __init__(self):
        super().__init__()
        self.base_url = 'https://mangakakalot.com'

    def search(self, query):
        if isinstance(query, BasicSearchQuery):
            query = query
        elif isinstance(query, ComicSearchConfig):
            query = str(query)
        else:
            raise TypeError('Invalid query parameter, expected type of BasicSearchQuery or ComicSearchConfig')

        response = requests.get(url=f'{self.base_url}/search/story/{query}', headers=headers)
        if not response.ok:
            return response
        soup = BeautifulSoup(response.content, "html.parser")
        
        