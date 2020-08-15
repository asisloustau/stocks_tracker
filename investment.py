import yfinance
from yfinance import Ticker
import datetime


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

        self.ticker = ticker

        self.amount = amount

        if isinstance(date, datetime.datetime):
            self.date = date
        else:
            self.date = datetime.datetime.strptime(date, "%m-%d-%Y")

        super().__init__(self.ticker)  # inherit __init__ from Ticker

    def __str__(self):
        return f"Investment({self.ticker},${self.amount},{self.date})"

    def __repr__(self):
        return self.__str__()

    # def get_stock_data(self):
