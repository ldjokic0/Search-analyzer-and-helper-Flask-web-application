from flask import Flask, redirect, render_template, request, session
from pull_data import kp_search
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

con = sqlite3.connect('SAH.db', check_same_thread=False)
db = con.cursor()

""" @app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response """

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        keyword = request.form.get("keyword")
        # Works just for kupujemprodajem for now
        website = request.form.get("selected_website")
        if not keyword:
            # TODO: Add invalid input notification
            return render_template("home.html")

        items, count = kp_search(keyword)
        #TODO: Add items to SQL database

        print(keyword, website, count)
        return render_template("home.html")
    else:
        return render_template("home.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    print("dada")
    if request.method == "POST":
        
        if not request.form.get("username"):
            return render_template("register.html", warning = True)

        # TODO: Add conditions for password (atleast 6 letters with alphanumeric and numeric characters), check if username already exists

        username = request.form.get("username")
        password = request.form.get("password")
        hash_password = generate_password_hash(password)

        db.execute("INSERT INTO users (username, hash_password) VALUES (?, ?)", (username, hash_password))
        con.commit()

        return render_template("home.html")

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html")
