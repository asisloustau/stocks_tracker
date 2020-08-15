import yfinance
from yfinance import Ticker
import datetime


class Investment(Ticker):

    def __init__(self, ticker, amount, date):
        """
        Initialize stock with required parameters:
            - ticker: ticker name
            - amount: amount invested
            - date: date of investment -datetime for now, will be input in MM-DD-YYYY
        """

        Ticker.__init__(self, ticker)

        self.amount = amount

        if isinstance(date, datetime.datetime):
            self.date = date
        else:
            self.date = datetime.datetime.strptime(date, "%m-%d-%Y")

    def __str__(self):
        return f"Investment({self.ticker},${self.amount},{self.date})"

    def __repr__(self):
        return self.__str__()

    # def get_stock_data(self):
