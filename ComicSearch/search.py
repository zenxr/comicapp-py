class ComicSearchConfig(object):
    def __init__(self, title = None, author = None, genre = None):
        self.title = title
        self.author = author
        self.genre = genre

class ComicSearch(object):
    def search(configuration):
        raise NotImplementedError('This method meant to be defined by derived class.')