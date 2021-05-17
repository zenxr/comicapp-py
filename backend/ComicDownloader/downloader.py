import configuration as config
import requests
import shutil
import os
from pathlib import Path
from bs4 import BeautifulSoup as soup
import multiprocessing

def download(urls, title, chapter, dir):
    # For every line in the file
    for idx, url in enumerate(urls):
        # Split on the rightmost / and take everything on the right side of that
        url = url.rstrip('\r\n')
        name = url.rsplit('/', 1)[-1]
        shortname = str(idx + 1) + name.rsplit('.', 1)[1]
        # if a chapter exists
        if chapter:
            filename = os.path.join(dir, title, chapter, shortname)
            # Combine the name and the downloads directory to get the local filename
        else:
            filename = os.path.join(dir, title, shortname)
        # ensure the directory exists
        directory = os.path.dirname(filename)
        if not os.path.exists(directory):
            Path(directory).mkdir(parents=True, exist_ok=True)
        # Download the file if it does not exist
        if not os.path.isfile(filename):
            response = requests.get(url, headers=config.headers)
            with open(filename, 'wb') as outfile:
                outfile.write(response.content)

def getLinks(url):
    response = requests.get(url, headers=config.headers)
    page_soup = soup(response.content, "html.parser")
    links = page_soup.findAll('img')

    # storylinks are images to be downloaded
    storylinks = []
    for link in links:
        # find the filename (everything after the last /)
        filename = link['src'].rsplit('/', 1)[-1]
        # remove the extension
        filename = os.path.splitext(filename)[0]
        # for the specific site being scraped
        # all relevant images only contain numbers
        if filename.isdigit():
            # for all numeric filenames, append to
            storylinks.append(link['src'])
     # if there are no chapters, then the url is formatted as
    # http://domain.com/title/page_num.extension
    # handle accordingly
    return storylinks

def getAllChapters(url):
    response = requests.get(url, headers=config.headers)
    page_soup = soup(response.content, "html.parser")
    chapter_list = page_soup.find("div", class_="panel-story-chapter-list")
    if not chapter_list:
        chapter_list = page_soup.find("div", class_='manga-info-chapter')
    possible_chapters = chapter_list.findChildren("a", href=True)
    chapters = {}
    for idx, chapter in enumerate(possible_chapters):
        chapters[str(idx).zfill(4)] = chapter['href']
    # TODO FIND BETTER WAY
    # for chapter in possible_chapters:
    #     chapters[chapter.text] = chapter['href']
    return chapters

def getSeries(url, directory):
    seriesname = url.rsplit('/', 1)[1]
    chapters = getAllChapters(url)
    for chapter in chapters:
        urls = getLinks(chapters[chapter])
        print("Title: " + seriesname + " Chap : " + chapter)
        download(urls, seriesname, chapter.replace(' ', '_'), directory)

def getSeriesMutliProc(url, directory):
    process = multiprocessing.Process(target=getSeries, args=(url, directory,))
    process.daemon = True
    process.start()

if __name__ == "__main__":
    getSeries('https://manganelo.com/manga/wp918498', config.download_dir)
    # getSeries(config.url, config.download_dir)
