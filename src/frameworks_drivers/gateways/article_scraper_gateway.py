""" Responsible to implement the logical to scraping the news site 
"""
import utils.date_utils
from entities.article_entity import Article
import utils.mappers_utils
from .article_params_gateway import ParamsGateway
from utils.values_utils import get_url_value
from frameworks_drivers.drivers.selenium_driver import CustomSelenium
import logging
import utils
from typing import Tuple
class ArticleScraper:
    """ Class of ArticleScraper, responsible to ensure the scraping of a article 
    """
    def __init__(self, search_params: ParamsGateway):
        self.search_params = search_params

    def scrape_news(self) -> list[Article]:
        """Function to scrape data from a news """
        logging.info("Starting Scraping.....")
        browser = CustomSelenium()
        browser.open_site(get_url_value())
        browser.search_phrase(self.search_params.phrase)
        categories_site = browser.get_categorys()
        categories_value, has_category = get_category_values(categories_site, self.search_params.categories)
        articles_data = browser.extract_useful_data_from_articles(
                             self.search_params.phrase,
                             utils.date_utils.return_current_month_plus_next_months(self.search_params.current_month_plus-1),
                             categories_value,
                             has_category
                             )
        return  convert_to_list_articles_entity(articles_data)


def get_category_values(categories_site: dict, categories_param: str) -> Tuple[list, bool]:
    checked_categories_values = []
    unchecked_categories = []
    try:   
        categories_selected = categories_param.split(',')
        for category_selected in categories_selected:
            formated_category_selected = str.upper(category_selected)
            if formated_category_selected in categories_site:
                checked_categories_values.append(categories_site[formated_category_selected])
            else:
                unchecked_categories.append(categories_selected)
        if checked_categories_values:
            return checked_categories_values, True

        if unchecked_categories:
            logging.warning("Categories not found: %s", ", ".join(unchecked_categories))        
        return None, False
    except AttributeError:
        logging.warning("Categories was not filled")
        return None, False

def convert_to_list_articles_entity(articles_data) -> list[Article]:
    article_entity_list : list[Article] = []
    for article_data in articles_data:
        article_entity_list.append(utils.mappers_utils.map_object_to_article_entity(
                title= article_data["title"],
                date= article_data["date"],
                description= article_data["description"],
                image_filename= article_data["image_filename"],
                search_count= article_data["search_count"],
                contains_money= article_data["contains_money"]
                ))
        

    return article_entity_list 