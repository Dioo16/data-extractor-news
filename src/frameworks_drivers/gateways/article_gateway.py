""" Article logical Implementation 

"""
from .article_scraper_gateway import ArticleScraper
from .article_params_gateway import ParamsGateway
from interfaces.gateways.article_interface import ArticleInterface
from entities.article_entity import Article

class ArticleGateway(ArticleInterface):
    """ Classe responsible for the implementation of the interface Article
    """
    def __init__(self, scraper: ArticleScraper ):
        self.scraper = scraper

    def return_articles(self) -> list[Article] :
        """ List[Article]: a list of articles"""
        return self.scraper.scrape_news()
    