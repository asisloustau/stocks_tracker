import yfinance
from yfinance import Ticker
from datetime import datetime, timedelta
import sqlite3

DB_NAME = 'investments.db'


class Investment(Ticker):
    """
    This class inherits Ticker from yfinance. We can use any of the attributes and methods from this class to return stock data from Yahoo Finance
    """

    def __init__(self, ticker, amount, date):
        """
        Initialize stock with required parameters:
            - ticker: ticker name
            - amount: amount invested
            - date: date of investment -datetime for now, will be input in MM-DD-YYYY
        """

        super().__init__(ticker)  # inherit __init__ from Ticker

        self.amount = amount

        if isinstance(date, datetime):
            self.date = date
        else:
            self.date = datetime.strptime(date, "%m-%d-%Y")

        # Get stock data from yfinance for dates starting the investment date
        self.data = self.history(start=self.date.strftime("%Y-%m-%d"))

        # convert Timestamp indexes to str datetime for sqlite
        # WARNING this will have to be changed in more robust sql engines to preserve date format
        self.data.index = self.data.index.strftime(
            "%Y-%m-%d") + f"_{self.ticker}"

    def __str__(self):
        return f"Investment({self.ticker},${self.amount},{self.date})"

    def __repr__(self):
        return self.__str__()

    def store_investment_data(self):

        # sqlite connect to database
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        # create investments table if not exists
        c.execute(
            """
                CREATE TABLE IF NOT EXISTS investments
                (
                    date_created text,
                    date_invested text,
                    ticker text,
                    amount real
                )
            """
        )

        # add investment to database
        current_date = datetime.now().strftime("%Y-%m-%d")
        c.execute(
            f"""
        INSERT INTO investments 
        VALUES (
            '{current_date}',
            '{self.date.strftime("%Y-%m-%d")}',
            '{self.ticker}',
            '{self.amount}'
            )
            """
        )

        # commit and close
        conn.commit()
        conn.close()

        return True

    def get_stock_data(self):
        """
        Return DataFrame with stock data for investment instance
        """
        return self.data

    def store_stock_data(self):
        """
        Populate database with stock historical data
        """

        # sqlite connect to database
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        # create investments table if not exists
        c.execute(
            """
                CREATE TABLE IF NOT EXISTS stock_history
                (
                    date text primary key,
                    open real,
                    high real,
                    low real,
                    close real,
                    volume int,
                    dividends int,
                    'stock splits' int
                )
            """
        )
        # store DataFrame in db table - careful, if existing dates in db, it will throw an error
        # TODO: either (1) add each df row independently and check if primary exists or (2) when filling new data make sure to check last value
        self.data.to_sql('stock_history', con=conn, if_exists='append')
        return True


# TODO:
# Fetch data from database and return a dataframe with, for each ticker in investments:
# figure out regex to join tables -date_ticker
# ticker | initial_value | current_value | profit_loss | profit_loss_pct (for now, can add more views/features)

# Any time user checks data:
# check current date
# check last available date in database for each ticker
# get data for all tickers found in database (yfinance.Tickers)
# store data in database (NOTE we could do some sort of class inheritance/mixin to use store_stock_data from investment)
