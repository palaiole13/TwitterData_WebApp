import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup

import csv
import sqlite3 as sql



# Configure application
app = Flask(__name__)


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///final.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    """Show main page"""
    ## TODO see if it's easy to categorise individual vs organisation vs company twitter accounts
    ## Enrich My_DATA
    ## Add history of searches
    ## Download button next to each db
    user_id = session["user_id"]
    if request.method == "POST":
        keyword = request.form.get("keyword")
        limit = request.form.get("limit", type=int)
        rows = lookup(keyword, limit)
        if rows == None:
            return apology("invalid keyword", 400)
        db.execute("DELETE FROM u_db WHERE id = ?", user_id)
        for i in rows["users"]:
            db.execute("INSERT INTO u_db (id, keyword, username, user_description, location, tweet, date, retweets, likes) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", user_id, keyword, i[0], i[1], i[2],
                   i[3], i[4], i[5], i[6])
        flash("Success!")
        return render_template("search_results.html", users = rows["users"], keyword = keyword)
    else:
        return render_template("index.html")


@app.route("/download")
@login_required
def download():
    # Export data into CSV file
    user_id = session["user_id"]
    conn = sql.connect('final.db')

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM u_db WHERE id = %s" % user_id)
    with open("u_db_data.csv", "w") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter="\t")
        csv_writer.writerow([i[0] for i in cursor.description])
        csv_writer.writerows(cursor)
        dirpath = os.getcwd() + "/u_db_data.csv"
        flash("Data exported Successfully into {}".format(dirpath))
    return redirect("/")


@app.route("/about")
@login_required
def about():
    return apology("TO DO")


@app.route("/mydata")
@login_required
def mydata():
    user_id = session["user_id"]
    u_rows = db.execute("SELECT * FROM u_db WHERE id = ?", user_id)

    return render_template("mydata.html", u_rows = u_rows)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # Forget any user_id
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        rows = db.execute("SELECT * FROM users")
        # Ensure username was submitted
        if not username:
            return apology("must provide username", 400)
        # Ensure username is available
        for row in rows:
            if username == row["username"]:
                return apology("username is not available", 400)
        # Ensure password was submitted
        if not password:
            return apology("must provide password", 400)
        #elif len(password) < 6 or not any(char.isdigit() for char in password):
         #   return apology("password must be at least 6 characters long and must include a number", 400)
        # Ensure password and confirmation match
        elif password != request.form.get("confirmation"):
            return apology("passwords don't match", 400)
        # hash the password
        hash = generate_password_hash(password)

        # Remember user
        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, hash)

        # Successful registration, you can now log in
        return redirect("/")

    # if request method GET
    else:
        return render_template("register.html")