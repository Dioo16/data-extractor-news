'''Possible categorys: Live Blogs, Photo Galleries, Sections, Stories, Subsections, Videos
'''
from frameworks_drivers.gateways.article_gateway import ArticleGateway
from frameworks_drivers.gateways.article_params_gateway import ParamsGateway
from frameworks_drivers.gateways.article_scraper_gateway import ArticleScraper
from frameworks_drivers.repositories.article_repository import ArticleRepository
from use_cases.extract_news import ExtractArticle

def main(phrase: str = None, category: str = None ,months: int = None) -> None:
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
    extract_news_use_case = ExtractArticle(article_gateway, article_repository, params)

    extract_news_use_case.execute()

if __name__ == '__main__':
    main()
