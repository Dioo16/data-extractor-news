'''Define the structure to save a article in the repository(excel in this case) '''
from abc import ABC, abstractmethod
from entities.article_entity import Article

class ArticleRepositoryInterface(ABC):
    """Class repository of an Article"""
    @abstractmethod
    def save_articles(self, articles: list[Article], search_phrase: str, month:int) -> None:
        """Save articles in the repository"""
