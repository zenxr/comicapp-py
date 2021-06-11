import requests
import json
import sys
import os
from bs4 import BeautifulSoup

from ComicSearch.search import ComicSearch, ComicSearchConfig, BasicSearchQuery

sys.path.append(os.path.abspath(os.path.join(__file__, '..', '..')))
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
            print('Something went wrong')
            return response
        soup = BeautifulSoup(response.content, "html.parser")
        result_list = soup.find('div', class_='panel_story_list')
        story_items = result_list.findChildren('div', class_='story_item')
        story_json = [self._get_story_item_json(si) for si in story_items]
        return json.dumps(story_json)

    def _get_story_item_json(self, story_item):
        result = {'title': '', 'author(s)': '', 'thumbnail': '', 'views': '', 'link':''}
        story_name_aref = story_item.find('h3', class_='story_name').find('a')
        result['title'] = story_name_aref.string
        result['link'] = story_name_aref['href']
        if story_item.find('img'):
            result['thumbnail'] = story_item.find('img')['src']
        story_details = story_item.find('div', class_='story_item_right')
        if story_details:
            spans = story_details.find_all('span')
            if spans:
                author_match = next(s for s in spans if 'Author' in s.text)
                result['author(s)'] = '' if not author_match else str(author_match.text).split(':', 1)[1].lstrip().rstrip()
                view_match = next(s for s in spans if 'View' in s.text)
                result['views'] = '' if not view_match else str(view_match.text).split(':', 1)[1].lstrip().rstrip()
        return result