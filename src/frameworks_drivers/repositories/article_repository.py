from datetime import datetime
from entities.article_entity import Article
from interfaces.repositories.article_repository_interface import ArticleRepositoryInterface
import utils.dir_utils
import utils.values_utils
import utils.date_utils
from openpyxl import Workbook

class ArticleRepository(ArticleRepositoryInterface):
    def save_articles(self, articles: list[Article], search_phrase: str, month: int) -> None:
        new_dir = create_dir_to_save_excel_and_images(search_phrase, month)
        xlsx_filename  = self.define_xlsx_filename(search_phrase, new_dir)
        move_images_to_new_dir_repository(new_dir)
        wb = Workbook()
        ws = wb.active
        ws.title = "Articles"

        ws.append(["Title", "Date", "Description", "Image Filename", "Search Count", "Contains Money"])

        for article in articles:
            ws.append([article.title, article.date, article.description, 
                       article.image_filename, article.search_count, article.contains_money])
        
        wb.save(xlsx_filename)


    @staticmethod
    def define_xlsx_filename(phrase_searched: str, new_dir: str) -> str:
        today = datetime.now().strftime("%m-%d-%Y")        
        return f"{new_dir}\\news_search_{phrase_searched}-{today}.xlsx"


def create_dir_to_save_excel_and_images(phrase_searched, month):
    from_date = utils.date_utils.return_current_month_plus_next_months(month-1).strftime("%m-%d-%Y")
    to_date = datetime.now().strftime("%m-%d-%Y")
    dir = utils.values_utils.get_output_dir_value()
    return utils.dir_utils.create_new_dir_to_save_excel_and_images(dir, from_date, to_date, phrase_searched)

def move_images_to_new_dir_repository(new_dir):
    src_dir = utils.values_utils.get_news_images_dir_value()
    utils.dir_utils.move_images_to_repository(new_dir, src_dir)