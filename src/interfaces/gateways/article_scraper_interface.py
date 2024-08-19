""" Define the method and what should return from a news scraping   """
from abc import ABC, abstractmethod
from entities.article_entity import Article

class ArticleScraperInterface(ABC):
    """Class scraper of an Article"""
    @abstractmethod
    def fetch_article(self, search_params) -> list[Article]:
        """fetch the article using the params"""
