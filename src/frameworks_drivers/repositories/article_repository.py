from datetime import datetime
from entities.article_entity import Article
from interfaces.repositories.article_repository_interface import ArticleRepositoryInterface
import utils.values_utils
from openpyxl import Workbook

class ArticleRepository(ArticleRepositoryInterface):
    def save_articles(self, articles: list[Article], search_phrase: str) -> None:
        xlsx_filename  = self.define_csv_filename(search_phrase)

        wb = Workbook()
        ws = wb.active
        ws.title = "Articles"

        ws.append(["Title", "Date", "Description", "Image Filename", "Search Count", "Contains Money"])

        for article in articles:
            ws.append([article.title, article.date, article.description, 
                       article.image_filename, article.search_count, article.contains_money])
        
        wb.save(xlsx_filename)


    @staticmethod
    def define_csv_filename(phrase_searched: str) -> str:
        today = datetime.now().strftime("%m-%d-%Y")
        dir = utils.values_utils.get_excel_dir_value()
        return f"{dir}\\news_search_{phrase_searched}-{today}.xlsx"
        
         