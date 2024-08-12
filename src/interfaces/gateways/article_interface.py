""" Define what a article should have"""
from abc import ABC, abstractmethod

class ArticleInterface(ABC):
    """Class  of an Article"""
    @abstractmethod
    def return_articles(self, search_params):
        """Return the articles"""
