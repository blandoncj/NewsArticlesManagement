"""
this file contains the NewspaperController class which is responsible
for handling the business logic of the newspaper entity.
"""

from dao.newspaper import NewspaperDao
from util.util import Util


class NewspaperController:
    """
    NewspaperController class
    """

    def __init__(self, db) -> None:
        self.dao = NewspaperDao(db)

    def get_all(self):
        """
        get_all method
        """
        return self.dao.get_all()

    def get_weekly_article_report(self):
        """
        get_weekly_article_report method
        """
        return self.dao.get_weekly_article_report()

    def save_article(self, article):
        """
        save_article method
        """
        self.dao.save_article(article)

    def validate_last_six_months_average(self, newspaper_id, articles):
        """
        validate_last_six_months_average method
        """
        return self.dao.validate_last_six_months_average(newspaper_id, articles)

    def populate_articles(self, days=180):
        """
        populate_articles method
        """
        newspapers = self.get_all()
        newspaper_ids = [newspaper.newspaper_id for newspaper in newspapers]
        Util.populate_articles(self.dao.db, newspaper_ids, days)
