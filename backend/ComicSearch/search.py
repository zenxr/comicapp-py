class ComicSearchConfig(object):
    def __init__(self, title = None, author = None, genre = None):
        self.title = title
        self.author = author
        self.genre = genre
    
    def to_basic_search_query(self):
        return BasicSearchQuery([self.title, self.author, self.genre])

class BasicSearchQuery(object):
    def __init__(self, words: list):
        self.words = words
    
    def __str__(self):
        return('_'.join(self.words))

class ComicSearch(object):
    def search(configuration):
        raise NotImplementedError('This method meant to be defined by derived class.')