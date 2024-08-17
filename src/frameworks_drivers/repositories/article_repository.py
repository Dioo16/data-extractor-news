from datetime import datetime
import logging
from entities.article_entity import Article
from interfaces.repositories.article_repository_interface import ArticleRepositoryInterface
import utils.dir_utils
import utils.values_utils
import utils.date_utils

from openpyxl import Workbook

class ArticleRepository(ArticleRepositoryInterface):
    def save_articles(self, articles: list[Article], search_phrase: str, month: int) -> None:
        dir = define_output_dir()
        xlsx_filename  = self.define_xlsx_filename(search_phrase, dir, month)
        wb = Workbook()
        ws = wb.active
        ws.title = "Articles"

        ws.append(["Title", "Date", "Description", "Image Filename", "Search Count", "Contains Money"])
        try:
            for article in articles:
                ws.append([article.title, article.date, article.description, 
                            article.image_filename, article.search_count, article.contains_money])
        except Exception as e:
            logging.error(f"Error to save article in database: {e}", e)
            
        wb.save(xlsx_filename)
        
    def save_articles_images(self) -> None:
        src_folder_images = utils.values_utils.get_news_images_dir_value()
        target_zip_folder = define_output_dir()
        utils.dir_utils.zip_folder(src_folder_images, target_zip_folder)
        

    @staticmethod
    def define_xlsx_filename(phrase_searched: str, dir: str, month: int) -> str:
        from_date = utils.date_utils.return_current_month_plus_next_months(month-1).strftime("%m-%d-%Y")
        to_date = datetime.now().strftime("%m-%d-%Y")
        return f"{dir}/news_search_{phrase_searched}_{from_date}_to_{to_date}.xlsx"


def define_output_dir():
    dir = utils.values_utils.get_output_dir_value()
    return dir 

