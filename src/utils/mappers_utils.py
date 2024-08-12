from entities.article_entity import Article
from datetime import datetime


def map_object_to_article_entity (
    title: str, 
    date:datetime, 
    description:str,
    image_filename:str,
    search_count: int,
    contains_money:bool
    ) -> Article:
    
    return Article(
        title= title,
        date= date,
        description= description,
        image_filename= image_filename,
        search_count= search_count,
        contains_money= contains_money
        )