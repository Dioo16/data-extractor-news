""" Article logical Implementation 

"""
from article_scraper_gateway import ArticleScraper
from interfaces.gateways.article_interface import ArticleInterface
from entities.article_entity import Article

class ArticleGateway(ArticleInterface):
    """ Classe responsible for the implementation of the interface

    Returns:
        List[Article]: a list of articles
"""
    def __init__(self, scraper: ArticleScraper ):
        self.scraper = scraper

    def return_articles(self, search_params) -> list[Article] :
        return self.scraper.scrape_news(search_params)
