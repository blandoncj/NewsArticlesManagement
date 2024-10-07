"""
this file contains the Util class which is used to populate the articles table with random data
"""

import random
import datetime
import MySQLdb


class Util:
    """
    Util class
    """

    @staticmethod
    def populate_articles(db, newspaper_ids, days=180):
        """
        populate_articles method
        """
        try:
            for i in range(days):
                date = datetime.datetime.today() - datetime.timedelta(days=i)
                article_count = random.randint(10, 20)
                newspaper_id = random.choice(newspaper_ids)
                with db.connection.cursor() as cursor:
                    cursor.execute(
                        """INSERT INTO articles (newspaper_id, date, article_count) 
                           VALUES (%s, %s, %s)
                        """,
                        (newspaper_id, date.strftime("%Y-%m-%d"), article_count),
                    )
            db.connection.commit()
        except MySQLdb.Error as e:
            print(f"Error populating articles: {e}")
