"""
this file contains the NewspaperDao class, which is responsible 
for handling all the database operations related to the newspapers table.
"""

import datetime
import MySQLdb
from models.newspaper import Newspaper


class NewspaperDao:
    """
    NewspaperDao class
    """

    def __init__(self, db):
        self.db = db

    def get_all(self):
        """
        get_all method
        """
        try:
            with self.db.connection.cursor() as cursor:
                cursor.execute("SELECT * FROM newspapers")
                return [Newspaper(row[1], row[0]) for row in cursor.fetchall()]
        except MySQLdb.Error as e:
            print(f"Error getting all newspapers: {e}")
            return None

    def get_weekly_article_report(self):
        """
        get_weekly_article_report method
        """
        try:
            with self.db.connection.cursor() as cursor:
                today = datetime.datetime.today()
                start_date = today - datetime.timedelta(days=6)

                query = """
                SELECT n.name AS newspaper_name, a.date AS day, SUM(a.article_count) AS total_articles
                FROM newspapers n
                JOIN articles a ON n.id = a.newspaper_id
                WHERE a.date >= %s AND a.date <= %s
                GROUP BY n.name, a.date
                ORDER BY a.date
                """

                cursor.execute(
                    query, (start_date.strftime("%Y-%m-%d"), today.strftime("%Y-%m-%d"))
                )
                report_data = cursor.fetchall()

                final_report = {}

                day_mapping = {
                    0: "Lunes",
                    1: "Martes",
                    2: "Miércoles",
                    3: "Jueves",
                    4: "Viernes",
                    5: "Sábado",
                    6: "Domingo",
                }

                for row in report_data:
                    newspaper_name = row[0]
                    day = row[1]
                    total_articles = row[2]
                    day_of_week = day.weekday()

                    if newspaper_name not in final_report:
                        final_report[newspaper_name] = {
                            "Lunes": 0,
                            "Martes": 0,
                            "Miércoles": 0,
                            "Jueves": 0,
                            "Viernes": 0,
                            "Sábado": 0,
                            "Domingo": 0,
                        }

                    final_report[newspaper_name][
                        day_mapping[day_of_week]
                    ] += total_articles

                ordered_report = {}
                days_of_week = [
                    "Lunes",
                    "Martes",
                    "Miércoles",
                    "Jueves",
                    "Viernes",
                    "Sábado",
                    "Domingo",
                ]

                for newspaper, days in final_report.items():
                    ordered_report[newspaper] = {
                        day: days[day] for day in days_of_week
                    }

                return ordered_report

        except MySQLdb.Error as e:
            print(f"Error getting weekly report: {e}")
            return None

    def save_article(self, article):
        """
        save_article method
        """
        try:
            with self.db.connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO articles (newspaper_id, article_count) VALUES (%s, %s)",
                    (article.newspaper_id, article.articles),
                )
                self.db.connection.commit()
        except MySQLdb.Error as e:
            print(f"Error saving article: {e}")
            return False

    def validate_last_six_months_average(self, newspaper_id, articles):
        """
        validate_last_six_months_average method
        """
        try:
            with self.db.connection.cursor() as cursor:
                query = """
                SELECT AVG(article_count) AS average
                FROM articles
                WHERE newspaper_id = %s AND date >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH)
                """

                cursor.execute(query, (newspaper_id,))
                average = cursor.fetchone()[0]

                if average is None:
                    return True
                return average <= articles

        except MySQLdb.Error as e:
            print(f"Error getting average: {e}")
            return None
