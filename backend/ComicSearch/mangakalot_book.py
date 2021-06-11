import requests
import json
import sys
import os
from bs4 import BeautifulSoup

sys.path.append(os.path.abspath(os.path.join(__file__, '..', '..')))
from configuration import headers

class MangakalotBook(object):
    def __init__(self, url):
        self.url = url

    def fetch_storyinfo(self, result, soup):
        book_panel = soup.find('div', class_='panel-story-info')
        book_image = book_panel.find('div', class_='story-info-left').find('img')

        if book_image:
            result['image'] = book_image['src']
        book_info = book_panel.find('div', class_='story-info-right')
        result['name'] = book_info.find('h1').text
        info_table = book_info.find('table', class_='variations-tableInfo')
        if info_table:
            rows = info_table.find_all('tr')
            author_row = next(r for r in rows if r.find('i', class_='info-author'))
            if author_row:
                result['authors'] = author_row.find('td', class_='table-value').find('a').text
            genre_row = next(r for r in rows if r.find('i', class_='info-genres'))
            if genre_row:
                genre_links = genre_row.find('td', class_='table-value').find_all('a')
                result['genres'] = ', '.join(l.text for l in genre_links)
        extended_info_table = book_info.find('div', class_='story-info-right-extent')
        if extended_info_table:
            rows = extended_info_table.find_all('p')
            updated_row = next(r for r in rows if r.find('i', class_='info-time'))
            if updated_row:
                result['updated'] = updated_row.find('span', class_='stre-value').text
            views_row = next(r for r in rows if r.find('i', class_='info-view'))
            if views_row:
                result['views'] = views_row.find('span', class_='stre-value').text
        book_description = book_panel.find('div', class_='panel-story-info-description')
        if book_description:
            result['description'] = book_description.text.split(':', 1)[1].lstrip()
        return result

    def fetch_mangainfo(self, result, soup):
        book_panel = soup.find('div', class_='manga-info-top')
        book_image = book_panel.find('div', class_='manga-info-pic').find('img')

        if book_image:
            result['image'] = book_image['src']
        book_info = book_panel.find('ul', class_='manga-info-text')
        result['name'] = book_info.find('h1').text
        book_info_items = book_info.findAll('li')
        author_block = next(li for li in book_info_items if 'Author' in li.text)
        if author_block:
            author_items = author_block.findAll('a', href=True)
            authors = [a.text for a in author_items]
            result['authors'] = ', '.join(authors)
        genre_block = next(li for li in book_info_items if 'Genre' in li.text)
        if genre_block:
            genre_items = genre_block.findAll('a', href=True)
            genres = [a.text for a in genre_items]
            result['genres'] = ', '.join(genres)
        updated_block = next(li for li in book_info_items if 'updated' in li.text.lower())
        if updated_block:
            result['updated'] = updated_block.text.split(':', 1)[1].lstrip().rstrip()
        view_block = next(li for li in book_info_items if 'View' in li.text)
        if view_block:
            views = view_block.text.split(':', 1)[1].lstrip().rstrip()
            result['views'] = views
        description_block = soup.find('div', {'id': 'noidungm'})
        if description_block:
            result['description'] = description_block.text.split(':', 1)[1]
        return result

    def fetch(self):
        result = {'url': self.url, 'name': '', 'image': '', 'genres': '', 'authors': '', 'description': '', 'views': '', 'updated': ''}
        response = requests.get(url=self.url, headers=headers)
        if not response.ok:
            print('Something went wrong')
            return response
        soup = BeautifulSoup(response.content, "html.parser")
        book_panel = soup.find('div', class_='panel-story-info')
        if book_panel:
            return self.fetch_storyinfo(result, soup)
        else:
            return self.fetch_mangainfo(result, soup)
