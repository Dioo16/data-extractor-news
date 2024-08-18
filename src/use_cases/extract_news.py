"""
Module for Extracting and Storing News Articles

This module defines the `ExtractArticle` class, which handles the extraction of news articles 
and their storage into a repository. The class relies on an article gateway to fetch the articles 
and an article repository to save both the articles and their associated images.

Classes:
    ExtractArticle: Manages the extraction and storage of news articles based on the provided 
                    search parameters.

Usage:
    The `ExtractArticle` class is used to encapsulate the logic for extracting news articles 
    and saving them to a specified repository. It interacts with the article gateway to obtain 
    articles and with the article repository to store the articles and images.

Dependencies:
    - `ArticleGateway`: Provides methods to fetch articles.
    - `ArticleRepository`: Provides methods to save articles and images.
    - `ParamsGateway`: Provides search parameters including the search phrase and time frame.
"""
from frameworks_drivers.gateways.article_gateway import ArticleGateway
from frameworks_drivers.repositories.article_repository import ArticleRepository
from frameworks_drivers.gateways.article_params_gateway import ParamsGateway

class ExtractArticle:
    """
    A class to handle the extraction and storage of news articles.

    This class is responsible for executing the article extraction process based on the 
    provided search parameters and storing the results into a repository. It interacts with 
    the article gateway to fetch articles and the article repository to save them along with 
    their images.

    Attributes:
        article_gateway (ArticleGateway): Gateway to fetch articles.
        article_repository (ArticleRepository): Repository to store articles and images.
        search_params (ParamsGateway): Parameters for the article search including phrase and 
        time frame.
    """
    def __init__(self,
                 article_gateway: ArticleGateway,
                 article_repository: ArticleRepository,
                 search_params: ParamsGateway):
        self.article_gateway = article_gateway
        self.article_repository = article_repository
        self.search_params = search_params

    def execute(self):
        """
        Executes the process of extracting and saving news articles.

        This method performs the following steps:
        1. Retrieves the search phrase and current month from the search parameters.
        2. Fetches articles from the article gateway.
        3. Saves the fetched articles and their images into the repository.

        Returns:
            None: This method does not return any value.
        """
        search_phrase = self.search_params.phrase
        month = self.search_params.current_month_plus
        articles = self.article_gateway.return_articles()
        self.article_repository.save_articles(articles, search_phrase, month)
        self.article_repository.save_articles_images()
