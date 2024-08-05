from entities.article_entity import Article
from interfaces.repositories.article_repository_interface import ArticleRepositoryInterface

class articleRepository(ArticleRepositoryInterface):
    def save_articles(self, article: list[Article]):

        #To do: Implement logical to put data in excel

        return 