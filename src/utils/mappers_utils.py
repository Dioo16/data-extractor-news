"""
Utility module for mapping data to article entities.

This module contains functions to map raw article data to the `Article` entity, which represents
an article with attributes such as title, date, description, image filename, search count, and
whether it contains money-related content.

Functions:
- map_object_to_article_entity: Maps provided article data to an `Article` entity.
"""
from datetime import datetime
from entities.article_entity import Article


def map_object_to_article_entity(
    title: str,
    date: datetime,
    description: str,
    image_filename: str,
    search_count: int,
    contains_money: bool
) -> Article:
    """
    Maps the provided article data to an `Article` entity.

    Args:
        title (str): The title of the article.
        date (datetime): The publication date of the article.
        description (str): The description of the article.
        image_filename (str): The filename of the article's image.
        search_count (int): The number of times the article was searched.
        contains_money (bool): Indicates if the article contains money-related content.

    Returns:
        Article: An instance of the `Article` entity populated with the provided data.
    """

    return Article(
        title=title,
        date=date,
        description=description,
        image_filename=image_filename,
        search_count=search_count,
        contains_money=contains_money
    )
