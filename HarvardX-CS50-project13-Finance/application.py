import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from time import gmtime, localtime, strftime

from helpers import apology, login_required, lookup, usd, User, input_check, regin_check, username_exists, isfloat


# API_KEY=pk_cbad111236c74b668ce59425b8e9ffee


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Create user
usr = User(db)

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/add_money", methods=["GET", "POST"])
@login_required
def add_money():
    """Add money to the account"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        cash = request.form.get("cash").replace(" ", "")

        # Check if can be converted to float
        if isfloat(cash):
            # If yes -> convert
            cash = float(cash)
        else:
            return render_template("apology1.html", apology="Format is not valid")

        # Check if cash is negative
        if cash < 0:
            return render_template("apology1.html", apology="Positive number required")

        # Add cash
        usr.add_cash(cash)

        return render_template("add-money-success.html", cash=cash)

    return render_template("add-money.html")


@app.route("/change_username", methods=["GET", "POST"])
@login_required
def change_username():

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        username = request.form.get("username").replace(" ", "")

        if not username:
            return render_template("apology1.html", apology="Provide new username")

        if username_exists(db, username):
            return render_template("apology1.html", apology="Username already exists")

        usr.change_username(username)
        session["username"] = usr.get_username()
        return render_template("success.html", msg="Username successfully updated!")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("change-username.html")


@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        curr_pass = request.form.get("current-password")
        new_pass = request.form.get("new-password")
        confirmation = request.form.get("confirmation")

        # Compare curr_pass with the existing
        if not check_password_hash(usr.get_hash(), curr_pass):
            return render_template("apology1.html", apology="Current password doesnt match!")

        # Check if password is confirmed
        if new_pass != confirmation:
            return render_template("apology1.html", apology="Password is not confirmed")

        # Change password
        usr.change_password(generate_password_hash(new_pass, method='pbkdf2:sha256', salt_length=8))

        return render_template("apology1.html", apology="Password successfully updated")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("change-password.html")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    if usr.shares_balance and usr.shares_owned() is None:
        return render_template("no-purchases.html", cash_balance=round(usr.cash_balance(), 3))
    else:
        # Get curren stock info for each share
        stock_info = [lookup(x) for x in usr.shares_owned()]

        # Get the count of all elements
        count = len(stock_info)

        # Get price for each holding (curr_price * shares_count)
        holdings = []
        for i in range(count):
            holdings.append(round(usr.shares_balance()[usr.shares_owned()[i]] * stock_info[i]["price"], 3))

        # Get grand total (stocks' total value + cash_balance)
        grand_total = sum(holdings) + usr.cash_balance()

        # Format to usd string
        holdings = [usd(x) for x in holdings]

        curr_price =[usd(x["price"]) for x in stock_info]
        # for x in stock_info:
        #     tmp.append(x[symbol])

        return render_template(
            "index.html",
            shares_owned=usr.shares_owned(),
            count=count,
            shares_balance=usr.shares_balance(),
            stock_info=stock_info,
            holdings=holdings,
            cash_balance=usd(usr.cash_balance()),
            grand_total=usd(grand_total),
            curr_price=curr_price)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        symbol = request.form.get("symbol").upper()
        share_count = request.form.get("shares")
        current_user = session["user_id"]

        # Validate input
        if input_check(symbol, share_count) != True:
            return input_check(symbol, share_count)

        # Convert shares to int
        share_count = int(share_count)

        # Get company name
        company = lookup(symbol)["name"]

        # Get share price
        share_price = lookup(symbol)["price"]

        # Calculate shares total price
        total_price = share_price * share_count

        money_left = 0
        # Check if the user can afford the number of shares at current price
        if total_price < usr.cash_balance():
            # Calculate the money left after the transaction
            money_left = usr.cash_balance() - total_price
        else:
            # Render apology
            return render_template("apology1.html", apology="Not enough minerals."), 400

        # Update the money left after the transaction
        usr.update_money(money_left)

        # Log stock into database
        db.execute("INSERT INTO stocks (symbol) VALUES(:symbol)", symbol=symbol)

        # Add purchase to database
        usr.add_purchase(symbol, share_price, share_count, "buy")

        usr.buy(symbol, share_count)

        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("buy.html")


@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""

    '''If the value of username is of length at least 1
    and does not already belong to a user in the database,
    the route should return, in JSON format, true,
    signifying that the username is (as of that moment) available'''

    # Get username
    username = request.args.get("username")

    if len(username) < 1:
        return jsonify(False)

    check_username = db.execute(
        "SELECT username FROM users WHERE username = :username", username=username)

    if len(check_username) == 0:
        return jsonify(True)
    else:
        return jsonify(False)


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    # Get list length
    length = len(usr.transactions())

    # Check if there is transaction history available
    if(length == 0):
        return render_template("no-history.html")

    # Keep stock_id:symbol here
    symbols = {}

    # Keep stock_id:company name here
    company = {}

    # Fill the dictionaries
    for pair in db.execute("SELECT * FROM stocks"):
        symbols[pair["stock_id"]] = pair["symbol"]
        company[pair["stock_id"]] = lookup(pair["symbol"])["name"]

    share_price = [usd(x["share_price"]) for x in usr.transactions()]
    return render_template("history.html", share_price=share_price, transactions=usr.transactions(), length=length, symbols=symbols, company=company)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        # Validate username and password
        if regin_check(username, password) != True:
            return regin_check(username, password)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            # return apology("invalid username and/or password", 403)
            return render_template("apology1.html", apology="Invalid username and/or password.")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Record current user id
        usr.current_user = session["user_id"]

        # Record current user username
        session["username"] = usr.get_username()

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


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    # Get the symbol entered by the user
    symbol = request.form.get("symbol")

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Check if the symbol is valid
        if lookup(symbol) is None:

            # return apology("Invalid symbol")
            return render_template("apology1.html", apology="Invalid symbol."), 400

        else:
            return render_template("quoted.html", name=lookup(symbol)["name"], price=usd(lookup(symbol)["price"]), symbol=lookup(symbol)["symbol"])

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Validate input
    if request.method == "POST":

        username = request.form.get("username").replace(" ", "")
        password = request.form.get("password").replace(" ", "")
        password_confirm = request.form.get("confirmation").replace(" ", "")

        # Validate username and password
        if regin_check(username, password) != True:
            return regin_check(username, password)

        elif not password_confirm:
            # return apology("must confirm password", 403)
            return render_template("apology1.html", apology="Must confirm password."), 400

        elif password != password_confirm:
            # return apology("password is not confirmed", 403)
            return render_template("apology1.html", apology="Password is not confirmed."), 400

        # Insert new user to the database
        result = db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)", username=username,
                                hash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8))

        # Ensure username is unique
        if not result:
            # return apology("username already exists")
            return render_template("apology1.html", apology="Username already exists."), 400

        return render_template("login.html")

    return render_template("register.html")




@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    # Get user's shares
    current_user = session["user_id"]

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Validate input
        if input_check(request.form.get("symbol"), request.form.get("shares")) != True:
            return input_check(request.form.get("symbol"), request.form.get("shares"))

        symbol = request.form.get("symbol").upper()
        share_count = request.form.get("shares")

        # Convert shares count to int
        share_count = int(share_count)

        # Get company name
        company = lookup(symbol)["name"]

        # Get share price
        share_price = lookup(symbol)["price"]

        # Calculate shares total price
        total_price = share_price * share_count

        # Check if the user is owner of the stocks
        if symbol in usr.shares_balance():

            # Check if the user has enough stocks to sell
            if usr.shares_balance()[symbol] < share_count:
                # return apology("Not enough shares")
                return render_template("apology1.html", apology="Not enough shares."), 400
            else:
                # usr.shares_balance()[symbol] -= share_count
                usr.sell(symbol, share_count)
            # Calculate the money after the transaction
            money_left = usr.cash_balance() + total_price
        else:
            # Render apology
            # return apology("These stocks are not yours")
            return render_template("apology1.html", apology="You don't have stock like these."), 400

        # Update the money left after the transaction
        usr.update_money(money_left)

        # Add purchase to database
        usr.add_purchase(symbol, share_price, share_count, "sell")

        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        if usr.shares_owned() is None:
            return render_template("sell.html", length=0, stock=usr.shares_owned())
        else:
            length = len(usr.shares_owned())
            return render_template("sell.html", length=length, stock=usr.shares_owned())


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
