"""
This module defines the main entry point for executing the news extraction use case.

It initializes and configures the necessary components for scraping and processing news articles
based on the provided parameters. The main function orchestrates the setup of various gateways
and repositories required for the extraction process and then invokes the use case to execute
the article extraction.

Modules:
- `ArticleGateway`: Handles interactions with the article data source.
- `ParamsGateway`: Manages the parameters used for scraping articles.
- `ArticleScraper`: Performs the scraping of articles based on the provided parameters.
- `ArticleRepository`: Manages the storage and retrieval of articles.
- `ExtractArticle`: Encapsulates the use case for extracting news articles.

Functions:
- `main`: Sets up the necessary components and executes the news extraction process.

Usage:
Run this module as the main program to start the article extraction process with default
or provided parameters.
"""
from frameworks_drivers.gateways.article_gateway import ArticleGateway
from frameworks_drivers.gateways.article_params_gateway import ParamsGateway
from frameworks_drivers.gateways.article_scraper_gateway import ArticleScraper
from frameworks_drivers.repositories.article_repository import ArticleRepository
from use_cases.extract_news import ExtractArticle


def main(
        phrase: str = None,
        category: str = None,
        months: int = None) -> None:
    """
    Main function to execute the news extraction use case.

    This function initializes the necessary components and orchestrates the process
    of scraping articles based on the provided search phrase, category, and time frame.

    Args:
        phrase (str, optional): The search phrase to filter the news articles. Defaults to "soccer".
        category (str, optional): The category to filter the news articles. If not provided, 
        no category filter is applied. months (int, optional): 
        The time frame in months to consider for the news articles. 
        Defaults to 1 if not provided or if the value is less than 1.

    Returns:
        None: This function does not return anything; 
        it triggers the execution of the news extraction process.
    """

    if phrase is None:
        phrase = ""
    if category is None:
        category = ""
    if months is None or months < 1:
        months = 1

    params = ParamsGateway(phrase, category, months)

    article_scraping = ArticleScraper(params)
    article_gateway = ArticleGateway(article_scraping)
    article_repository = ArticleRepository()
    extract_news_use_case = ExtractArticle(
        article_gateway, article_repository, params)

    extract_news_use_case.execute()


if __name__ == '__main__':
    main()
