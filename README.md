# stocks_tracker
Keep track of your profit/loses in the stock market

# Ideas

## Stock market daily data
From `yfinance` Python package
We can populate db with historical data if we want to make predictions

## Phase 1: MVP - CLI tool
### User input:
1. Stock ticker
2. Either (1) current value or (2) value invested at certain date

### Database (SQLite):
1. Table investments:
  - ticker (Primary Key), buy_amount, date
2. Table stock data:
  - TODO: Determine all features. For now:
  - (Surrogate Key) ticker (Foreign Key),date, open, high, low, close, volume
  
### Usage
- User inputs investment data --> database gets populated with stock data for all dates starting the date of investment -or earlier.
- User checks data function --> sql queries to check data from db
  - `summary` returns all investments
  - `ticker [tickername]` returns data for one specific ticker
