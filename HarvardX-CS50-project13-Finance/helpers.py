import os
import requests
import urllib.parse
import ast
import json
from time import gmtime, localtime, strftime

from flask import redirect, render_template, request, session
from functools import wraps
from ast import literal_eval


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def lookup(symbol):
    """Look up quote for symbol."""

    try:
        api_key = os.environ.get("API_KEY")
        response = requests.get(f"https://cloud-sse.iexapis.com/stable/stock/{urllib.parse.quote_plus(symbol)}/quote?token={api_key}")
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        quote = response.json()
        return {
            "name": quote["companyName"],
            "price": float(quote["latestPrice"]),
            "symbol": quote["symbol"]
        }
    except (KeyError, TypeError, ValueError):
        return None


def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"


# Validate input for the buy and sell sections
def input_check(symbol, share_count):

     # Check if field is empty
    if symbol == "" or symbol == None:
        # return apology("Please enter symbol",444)
        return render_template("apology1.html", apology="Please enter symbol."), 400

    # Check if stock symbol is valid
    elif lookup(symbol) is None:
        # return apology("Invalid stock",444)
        return render_template("apology1.html", apology="Invalid stock."), 400

    # Check if number of shares is digit
    elif not share_count.isdigit():
        # return apology("Positive integer required")
        return render_template("apology1.html", apology="Positive integer required."), 400

    # Check if number of shares is positive number
    elif int(share_count) < 0:
        # return apology("Positive integer required")
        return render_template("apology1.html", apology="Positive integer required."), 400
    else:
        return True


# Validate input for the register and login sections
def regin_check(username, password):

    if not username:
        # return apology("must provide username", 403)
        return render_template("apology1.html", apology="Must provide username."), 400
    elif not password:
        # return apology("must provide password", 403)
        return render_template("apology1.html", apology="Must provide password."), 400
    else:
        return True


# Check if username is in database
def username_exists(db, username):
    result = db.execute("SELECT * FROM users WHERE EXISTS(SELECT * FROM users WHERE username = :username )", username=username)

    if result:
        # username exists
        return True

    else:
        # username is free
        return False

# Check if is float
def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


class User:
    def __init__(self, db):
        self.db = db
        self.current_user = 0

    # Get the count for each share
    # list: [{'mysum': 4}, {'mysum': 3}, {'mysum': 1}, {'mysum': 2}, {'mysum': 1}]
    def shares_count(self):
        return self.db.execute('''SELECT SUM(share_count) AS mysum FROM purchases
                                WHERE (user_id = :current_user AND action="+")
                                GROUP BY share_id''', current_user=self.current_user)

    # Get user’s current cash balance
    def cash_balance(self):
        return self.db.execute(
            "SELECT cash FROM users WHERE id = :current_user", current_user=self.current_user)[0]["cash"]

    def buy(self, symbol, count):

        # Convert the symbol to upper case
        symbol = symbol.upper()

        # Init empty dict
        shares_dict = {}

        # Request DB for the string with shares and their count
        shares_count = self.db.execute(
            "SELECT shares_count FROM shares_balance WHERE user_id = :current_user", current_user=self.current_user)

        # Check if there is existing record
        # If true -> update the count of the shares
        if shares_count:

            # Convert to dictionary
            shares_dict = literal_eval(shares_count[0]["shares_count"])

            # Check if current symbol is in dictionary
            # If true -> update value
            if symbol in shares_dict:
                shares_dict[symbol] += count

            # Else -> this is the first buy -> add it to the dictionary
            else:
                shares_dict[symbol] = count

        # Else -> this is the first buy -> add it to the database
        else:
            shares_dict[symbol] = count
            self.db.execute("INSERT INTO shares_balance (user_id, shares_count) VALUES(:user_id, :shares_dict)",
                            user_id=self.current_user, shares_dict=json.dumps(shares_dict))

        # Update shares and their count in the DB
        self.db.execute("UPDATE shares_balance SET shares_count = :shares_dict WHERE user_id=:current_user",
                        shares_dict=json.dumps(shares_dict), current_user=self.current_user)

        #return shares_dict


    def sell(self, symbol, count):

        # Convert symbol to upper case
        symbol = symbol.upper()

        # Init empty dict
        shares_dict = {}

        # Request DB for the string with shares and their count
        shares_count = self.db.execute(
            "SELECT shares_count FROM shares_balance WHERE user_id = :current_user", current_user=self.current_user)

        shares_dict = self.shares_balance()
        shares_dict[symbol] -= count

        if shares_dict[symbol] == 0:
            del shares_dict[symbol]

         # Update shares and their count in the DB
        self.db.execute("UPDATE shares_balance SET shares_count = :shares_dict WHERE user_id=:current_user",
                        shares_dict=json.dumps(shares_dict), current_user=self.current_user)

    # Combine shares and their count into dictionary
    def shares_balance(self):

        # Request DB for the string with shares and their count
        shares_count = self.db.execute(
            "SELECT shares_count FROM shares_balance WHERE user_id = :current_user", current_user=self.current_user)

        # If it is a valid request(the record exists)
        if shares_count:

            # Convert the string to dictionary an return it
            shares_dict = literal_eval(shares_count[0]["shares_count"])
            return shares_dict

        # Return None if there is no record
        else:
            return None

    # Get all the shares owned by the user
    def shares_owned(self):

        # If the balance is not None(valid)
        if self.shares_balance():

            # Get the dict keys and return them as a list
            return list(self.shares_balance())  # ['F', 'D', 'NFLX']

        # User doesn't own ani shares
        else:
            return None

    # Update the money left after the transaction
    def update_money(self, money_left):
        self.db.execute("UPDATE users SET cash = :money_left WHERE id = :user_id", money_left=money_left, user_id=self.current_user)

    # Add purchase to database
    def add_purchase(self, symbol, share_price, share_count, action):
        self.db.execute('''INSERT INTO purchases (user_id, share_id, share_price, share_count, action, date)
                    VALUES (:user_id, :share_id, :share_price, :share_count, :action ,:date)''',
                        user_id=self.current_user,
                        share_id=self.db.execute(
                            "SELECT stock_id FROM stocks WHERE symbol = :symbol",
                            symbol=symbol)[0]["stock_id"],
                        share_price=share_price,
                        share_count=share_count,
                        action=action,
                        date=strftime("%a, %d %b %Y %H:%M:%S", gmtime()))

    # Select all transactions info
    def transactions(self):
        return self.db.execute("SELECT * FROM purchases WHERE user_id = :current_user", current_user=self.current_user)

    # Get username from database
    def get_username(self):
        return self.db.execute("SELECT username FROM users WHERE id = :current_user", current_user=self.current_user)[0]["username"]


    # Update current user username in database
    def change_username(self, new):
        self.db.execute("UPDATE users SET username = :new WHERE id = :user_id", new=new, user_id=self.current_user)

    # Add cash to the balance
    def add_cash(self, cash):
        self.db.execute("UPDATE users SET cash = :new_cash WHERE id = :current_user",
                        new_cash=cash + self.cash_balance(), current_user=self.current_user)

    # Get password hash
    def get_hash(self):
        return self.db.execute("SELECT hash FROM users WHERE id = :current_user", current_user=self.current_user)[0]["hash"]

    # Change password
    def change_password(self, new_pass):
        self.db.execute("UPDATE users SET hash = :new_pass WHERE id = :current_user",
                        new_pass=new_pass, current_user=self.current_user)

