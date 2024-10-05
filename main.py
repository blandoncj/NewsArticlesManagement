"""
this file is the main file of the project, it contains the routes of the application
"""

import datetime
from flask import Flask, flash, redirect, render_template, request, url_for
from flask_mysqldb import MySQL

from config import config
from controllers.newspaper import NewspaperController
from models.article import Article


app = Flask(__name__)

db = MySQL(app)


@app.route("/")
def home():
    """
    This function renders the index.html template
    """
    return render_template("index.html")


@app.route("/upload-article", methods=["GET", "POST"])
def upload_article():
    """
    This function renders the upload_article.html template
    """
    newspaper_controller = NewspaperController(db)

    if request.method == "POST":
        newspaper_id = request.form["newspaper"]
        articles = int(request.form["articles"])

        article = Article(newspaper_id, articles)

        if articles <= 0:
            flash("La cantidad de artículos debe ser mayor a 0", "error")
            return redirect(url_for("upload_article"))

        if not articles.is_integer():
            flash("La cantidad de artículos debe ser un número entero", "error")
            return redirect(url_for("upload_article"))

        if not newspaper_controller.validate_last_six_months_average(
            newspaper_id, articles
        ):
            flash("El promedio de artículos no es válido", "error")
            return redirect(url_for("upload_article"))

        newspaper_controller.save_article(article)
        flash("Artículo guardado correctamente", "success")
        return redirect(url_for("upload_article"))

    newspaper_controller = NewspaperController(db)
    newspapers = newspaper_controller.get_all()
    return render_template("upload_article.html", newspapers=newspapers)


@app.route("/populate-table")
def populate_table():
    """
    This function populates the articles table with random data
    """
    newspaper_controller = NewspaperController(db)
    newspaper_controller.populate_articles()
    flash("Artículos generados correctamente", "success")
    return redirect(url_for("upload_article"))


@app.route("/weekly-report", methods=["GET"])
def weekly_report():
    """
    This function renders the weekly_report.html template
    """
    newspaper_controller = NewspaperController(db)
    reports = newspaper_controller.get_weekly_article_report()
    today = datetime.datetime.today()

    days_names = [
        "Lunes",
        "Martes",
        "Miércoles",
        "Jueves",
        "Viernes",
        "Sábado",
        "Domingo",
    ]
    days = [today - datetime.timedelta(days=i) for i in range(7)]

    days_spanish = [days_names[day.weekday()] for day in days]

    return render_template(
        "weekly_report.html", reports=reports, column_days=days_spanish, days=days
    )


if __name__ == "__main__":
    app.config.from_object(config["development"])
    app.run()
