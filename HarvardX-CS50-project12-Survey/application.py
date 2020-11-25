# import cs50
import csv

from flask import Flask, jsonify, redirect, render_template, request

# Configure application
app = Flask(__name__)
# FLASK_APP = 'survey'

# Reload templates when they are changed
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.after_request
def after_request(response):
    """Disable caching"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET"])
def get_index():
    return redirect("/form")


@app.route("/form", methods=["GET"])
def get_form():
    return render_template("form.html")


@app.route("/form", methods=["POST"])
def post_form():
    if not request.form.get("last"):
        return render_template("error.html", message="You should enter your last name")
    if not request.form.get("email"):
        return render_template("error.html", message="You should enter your email")

    with open('survey.csv', 'a', newline='') as csvfile:
        spamwriter = csv.writer(csvfile)
        spamwriter.writerow([request.form.get("first")] +
                            [request.form.get("last")] +
                            [request.form.get("gender")] +
                            [request.form.get("email")] +
                            [request.form.get("city")] +
                            [request.form.get("district")])
    return get_sheet()


@app.route("/sheet", methods=["GET"])
def get_sheet():
    answers = []
    with open('survey.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            answers.append(row)

    count = len(answers)
    return render_template("sheet.html", answers=answers, count=count)

