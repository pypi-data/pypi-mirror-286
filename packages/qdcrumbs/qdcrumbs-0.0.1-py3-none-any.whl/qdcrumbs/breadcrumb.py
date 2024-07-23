#Breadcrumb container
class Breadcrumb:
    __slots__ = ['url','text']
    def __init__(self, url, text):
        self.url = url
        self.text = text