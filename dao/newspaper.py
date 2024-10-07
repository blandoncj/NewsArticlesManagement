"""
this file contains the NewspaperDao class, which is responsible 
for handling all the database operations related to the newspapers table.
"""

import datetime
from decimal import Decimal
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
                    ordered_report[newspaper] = {day: days[day] for day in days_of_week}

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
                    (article.newspaper_id, article.articles_count),
                )
                self.db.connection.commit()
                return self.validate_last_six_months_average(
                    article.newspaper_id, article.articles_count
                )
        except MySQLdb.Error as e:
            print(f"Error saving article: {e}")
            return False

    def validate_last_six_months_average(
        self, newspaper_id, articles, threshold_percentage=0.8
    ):
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

                threshold = Decimal(average) * Decimal(threshold_percentage)
                threshold = round(threshold, 2)
                return {"success": articles >= threshold, "treshold": threshold}

        except MySQLdb.Error as e:
            print(f"Error getting average: {e}")
            return None

    def calculate_coefficient_of_variation(self, newspaper_id):
        """
        calculate_coefficient_of_variation method
        """
        try:
            with self.db.connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT AVG(article_count) AS average, STDDEV(article_count) AS standard_deviation
                    FROM articles 
                    WHERE newspaper_id = %s
                    AND date >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH)
                """,
                    (newspaper_id,),
                )

                average, standard_deviation = cursor.fetchone()

                if average is None:
                    return None

                coefficient_variation = (
                    float(standard_deviation) / float(average)
                ) * 100
                return coefficient_variation
        except MySQLdb.Error as e:
            print(f"Error getting coefficient of variation: {e}")
            return None

    def calculate_interquartile_range(self, newspaper_id, article_count):
        try:
            with self.db.connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT COUNT(*) FROM articles
                    WHERE newspaper_id = %s
                    AND date >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH)
                """,
                    (newspaper_id,),
                )
                total = cursor.fetchone()[0]

                if total == 0:
                    return None, None

                q1 = int(total * 0.25)
                q3 = int(total * 0.75)

                cursor.execute(
                    """
                    SELECT article_count FROM articles
                    WHERE newspaper_id = %s
                    AND date >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH)
                    ORDER BY article_count
                    LIMIT 1 OFFSET %s
                               """,
                    (newspaper_id, q1),
                )
                q1_value = cursor.fetchone()[0] + article_count

                cursor.execute(
                    """
                    SELECT article_count FROM articles
                    WHERE newspaper_id = %s 
                    AND date >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH)
                    ORDER BY article_count
                    LIMIT 1 OFFSET %s
                               """,
                    (newspaper_id, q3),
                )
                q3_value = cursor.fetchone()[0] + article_count

                total = q3_value - q1_value
                return q1_value, q3_value, total
        except MySQLdb.Error as e:
            print(f"Error getting interquartile range: {e}")
            return None, None, None

    def analyze_variability(self, newspaper_id, article_count, high_threshold=40):
        cv = self.calculate_coefficient_of_variation(newspaper_id)
        cv = round(cv, 2)

        if cv is None:
            return "No se pudo calcular el coeficiente de variación."

        if cv > high_threshold:
            q1, q3, iqr = self.calculate_interquartile_range(
                newspaper_id, article_count
            )

            if q1 is not None and iqr is not None:
                return {
                    "variabilidad": "alta",
                    "cv": cv,
                    "q1": q1,
                    "q3": q3,
                    "iqr": iqr,
                }
            else:
                return "No se pudo calcular el rango intercuartil."
        else:
            return {"variabilidad": "baja", "cv": cv}
