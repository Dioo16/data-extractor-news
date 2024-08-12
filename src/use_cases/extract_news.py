from frameworks_drivers.gateways.article_gateway import ArticleGateway
from frameworks_drivers.repositories.article_repository import ArticleRepository
from frameworks_drivers.gateways.article_params_gateway import ParamsGateway

class ExtractArticle:
    def __init__(self, article_gateway: ArticleGateway, article_repository: ArticleRepository, search_params: ParamsGateway):
        self.article_gateway = article_gateway
        self.article_repository = article_repository
        self.search_params = search_params

    def execute(self):
        articles = self.article_gateway.return_articles()
        search_phrase = self.search_params.phrase
        month = self.search_params.current_month_plus
        self.article_repository.save_articles(articles, search_phrase, month)
