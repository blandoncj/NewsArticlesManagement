from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL, MySQLdb

from config import config


app = Flask(__name__)

db = MySQL(app)


@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.config.from_object(config["development"])
    app.run()
