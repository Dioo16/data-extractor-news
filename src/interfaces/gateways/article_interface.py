""" Define what a article should have"""
from abc import ABC, abstractmethod
from entities.article_entity import Article

class ArticleInterface(ABC):
    """Class  of an Article"""
    @abstractmethod
    def return_articles(self, search_params) -> list[Article]:
        """Return the articles"""
