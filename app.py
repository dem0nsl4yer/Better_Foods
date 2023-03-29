from pickletools import read_string1
from typing import Counter
import googlemaps
from yelpapi import YelpAPI
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from haversine import haversine, Unit
from helpers import apology, login_required, lookup
import datetime

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
API_KEY = open('API_KEYf.txt').read()

#initializing counter 
counter = 0
d= []
dY = []
t='aa'

# This is storing GMAPS keyVal. 
API_KEY1 = open('API_KEY.txt').read()
map_client = googlemaps.Client(API_KEY1)

# This is storing YELP keyVal. 
API_KEY = open('YELP_KEY.txt').read()
yelp_api = YelpAPI(API_KEY, timeout_s=3.0)

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    vis = db.execute("SELECT * FROM reviews WHERE user_id = ? ORDER BY yrating DESC", session["user_id"])
    return render_template("history.html", tran = vis)


@app.route("/visit", methods=["GET", "POST"])
@login_required
def visit():
    global d, dY
    if request.method =="POST":
    # split place id by Gmaps or Yelp. 
        c = request.form.get("symbol")
        r = request.form.get("rat")
        l = request.form.get("lev")
        n = request.form.get("nam")
        z = n.replace("%", " ")
        s = request.form.get("search")
        if not c:
            return apology("missing visit", 400)
        else:
            x = datetime.datetime.now()
            time = x.strftime("%c")
            db.execute("INSERT INTO visits (user_id, place_id, rsource, name, rating, level, time) VALUES(?, ?, ?, ?, ?, ?, ?)", session["user_id"], c, s, z, r, l, time)
            vis = db.execute("SELECT * FROM visits WHERE user_id = ?", session["user_id"])
            return render_template("review_static.html", vis= vis)
    else:
        return render_template("log_visit.html", d=d, dY=dY)
  #  return apology("TODO")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    tran = db.execute("SELECT * FROM reviews WHERE user_id = ? ORDER BY yrating DESC", session["user_id"])
    return render_template("history.html", tran = tran)


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
            return apology("must provide username and password", 403)

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
    # Cleaning up global variables. 
    global counter 
    conter = 0
    global d, dY
    d = []
    dY= []
    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/search", methods=["GET", "POST"])
@login_required
def quote():
    # saving post query
    global counter, d, dY
    c = request.form.get("symbol")
    t = []
    """Get stock quote."""
    # Checking if symbol provided
    if request.method =="POST":
        counter = 1
        if not c:
            return apology("missing symbol", 400)
    # Rendering quote
        else:
            c = request.form.get("symbol")
            gr = map_client.geocode(address=c)
            grd = gr[0]['geometry']['location']
            gr1 = (grd['lat'], grd['lng'])
            response = map_client.places_nearby(location=grd, radius = '1000', type = 'restaurant')
            respy =  yelp_api.search_query(location=c, sort_by="distance")
            resulY = respy.get('businesses')

    # Pulling data for YELP.
            for results in resulY:
                d1= results['coordinates']
                d0 = (d1['latitude'], d1['longitude'])
                dd = int(haversine(gr1, d0, unit=Unit.METERS))
                results['ds'] = dd
                results['or'] = c
                results['S'] = 'Y'
                try: 
                    results['rating']
                except KeyError:
                    results['rating'] = 0
                try:
                    level = len(f"{results['price']}")
                except KeyError:
                    level = 0
                results['price'] = level
            tY=sorted(resulY, key = lambda item: item['rating'], reverse=True)
            dY.extend(tY)
            dY=sorted(dY, key = lambda item: item['rating'], reverse=True)

    # Pulling data for google Maps. 
            resul = response.get('results')
            for results in resul:
                d1= results['geometry']['location']
                d0 = (d1['lat'], d1['lng'])
                dd = int(haversine(gr1, d0, unit=Unit.METERS))
                results['ds'] = dd
                results['or'] = c
                results['S'] = 'G'
                try: 
                    results['rating']
                except KeyError:
                    results['rating'] = 0
            t=sorted(resul, key = lambda item: item['rating'], reverse=True)
            d.extend(t)
            d=sorted(d, key = lambda item: item['rating'], reverse=True)
            return render_template("search_res.html", t=t, tY=tY)
    elif request.method !="POST" and counter != 0:
        return render_template("search_static.html", t=d, dY=dY)
    else:
        return render_template("search.html")
 #   return apology("TODO")

@app.route("/detail", methods=["GET", "POST"])
@login_required
def quotep():
    # saving post query
    """Get stock quote."""
    # Checking if symbol provided
    if request.method =="POST":
        c = request.form.get("test")
        s = request.form.get("search")
        print(s)
        if not c:
            return apology("missing symbol", 400)
    # Rendering quote
        elif s == 'G':
            name = request.form.get("name")
            z = name.replace("%", " ")
            gr = map_client.place(place_id=c)
            return render_template("detail.html", gr=gr, z=z)
        else:
            name = request.form.get("name")
            url = request.form.get("url")
            r = request.form.get("r")
            z = name.replace("%", " ")
            gr = yelp_api.reviews_query(id=c)
            return render_template("detailY.html", gr=gr, z=z, url = url, r=r)
    else:
        return render_template("search.html")
 #   return apology("TODO")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
    # Ensure username and password and confirmation submitted
        if not request.form.get("username") or not request.form.get("password") or not request.form.get("confirmation"):
            return apology("must provide username and password", 400)
    # Ensure password matched to confirmation
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords dont match", 400)
    # Ensure checking db for existing username
        else:
            rowT = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
            if not rowT:
                hash = generate_password_hash(request.form.get("password"))
    # Once username not in db, rendering the new user id
                db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", request.form.get("username"), hash)
    # Sending user to login page.
                return render_template("login.html")
            else:
                return apology("username alredy exists", 400)
    else:
        return render_template("register.html")
    # return apology("TODO")


@app.route("/review", methods=["GET", "POST"])
@login_required
def sell():
    global t
    vis = db.execute("SELECT * FROM visits WHERE user_id = ?", session["user_id"])
    if request.method == "POST":
        t = request.form.get("test")
        n = request.form.get("name").replace("%", " ")
        r = request.form.get("rat")
        l = request.form.get("lev")
        s = request.form.get("source")
        time = request.form.get("time")
        return render_template("upload_rev.html", n=n,r=r, l=l, t=t, time=time, s=s)
    else:
        return render_template("review.html", vis= vis)

@app.route("/add", methods=["GET", "POST"])
@login_required
def sello():
    global t
    vis = db.execute("SELECT * FROM visits WHERE user_id = ?", session["user_id"])
    if request.method == "POST":
        rev = request.form.get("review")
        yrat = request.form.get("rating")
        n = request.form.get("nam")
        r = request.form.get("gr")
        l = request.form.get("l")
        s = request.form.get("source")
        x = datetime.datetime.now()
        time = x.strftime("%c")
        db.execute("INSERT INTO reviews (user_id, place_id, name, rsource, rating, level, time, yreview, yrating) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", session["user_id"], t, n, s, r, l, time, rev, yrat)
        db.execute("DELETE FROM visits WHERE user_id = ? and place_id = ?", session["user_id"], t)
        return redirect("/history")
    else:
        return render_template("review.html", vis= vis)
