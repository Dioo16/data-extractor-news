""" Responsible to implement the logical to scraping the news site 
"""
from entities.article_entity import Article

class ArticleScraper:
    """ Class of ArticleScraper, responsible to ensure the scraping of a article 

    """
    def __init__(self, search_params):
        self.search_params = search_params

    def scrape_news(self) -> list[Article]:
        """Function to scrape data from a news """
        #To do
