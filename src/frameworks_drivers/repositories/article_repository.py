"""
Module for handling article data storage and management.

This module provides functionality to save articles to an Excel file, zip image files, 
and define file paths for output directories and filenames. It implements the 
ArticleRepositoryInterface to interact with article data.
"""
from datetime import datetime
import logging
from openpyxl import Workbook

from entities.article_entity import Article
from interfaces.repositories.article_repository_interface import ArticleRepositoryInterface
import utils.dir_utils
import utils.values_utils
import utils.date_utils



class ArticleRepository(ArticleRepositoryInterface):
    """
    Repository for managing and storing articles.

    Implements the methods to save articles to an Excel file and manage article images.
    """
    def save_articles(
            self,
            articles: list[Article],
            search_phrase: str,
            month: int) -> None:
        """
        Saves a list of articles to an Excel file.

        Args:
            articles (list[Article]): List of Article objects to save.
            search_phrase (str): Search phrase used for the filename.
            month (int): The month to be included in the filename.
        """
        output_dir = define_output_dir()
        xlsx_filename = self.define_xlsx_filename(search_phrase, output_dir, month)
        wb = Workbook()
        ws = wb.active
        ws.title = "Articles"

        ws.append(["Title",
                   "Date",
                   "Description",
                   "Image Filename",
                   "Search Count",
                   "Contains Money"])
        try:
            for article in articles:
                ws.append([article.title,
                           article.date,
                           article.description,
                           article.image_filename,
                           article.search_count,
                           article.contains_money])
        except ImportError as exception:
            logging.error("Error to save article in database: %s", exception)

        wb.save(xlsx_filename)

    def save_articles_images(self) -> None:
        """
        Zips and saves images associated with articles.
        """
        src_folder_images = utils.values_utils.get_news_images_dir_value()
        target_zip_folder = define_output_dir()
        utils.dir_utils.zip_folder(src_folder_images, target_zip_folder)

    @staticmethod
    def define_xlsx_filename(
            phrase_searched: str,
            src_dir: str,
            month: int) -> str:
        """
        Defines the filename for the Excel file based on search parameters.

        Args:
            phrase_searched (str): The search phrase used in the filename.
            src_dir (str): The directory where the file will be saved.
            month (int): The month range to include in the filename.

        Returns:
            str: The generated filename.
        """
        from_date = utils.date_utils.return_current_month_plus_next_months(
            month - 1).strftime("%m-%d-%Y")
        to_date = datetime.now().strftime("%m-%d-%Y")
        return f"{src_dir}/news_search_{phrase_searched}_{from_date}_to_{to_date}.xlsx"


def define_output_dir():
    """
    Retrieves the directory path for output files.

    Returns:
        str: The directory path for saving output files.
    """
    output_dir = utils.values_utils.get_output_dir_value()
    return output_dir
