import requests
from bs4 import BeautifulSoup

from .search import ComicSearch, ComicSearchConfig
from configuration import headers

class MangakalotSearch(ComicSearch):
    def __init__(self):
        super().__init__()
        self.base_url = 'https://mangakakalot.com'

    def search(configuration):
        response = requests.get(self.base_url, headers=headers)
        if not response.ok:
            return response
        soup = BeautifulSoup(response.content, "html.parser")
        
        