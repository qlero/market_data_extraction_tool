# market_data_extraction_tool
market_data_extraction_tool is a script that downloads:
- intraday (past 5 days)
- daily (past 5 years)
- active calls/puts of publicly traded companies.

### Installation
market_data_extraction_tool requires Python 3.x to run. It uses the following modules:

> cd market_data_extraction_tool

> pip install --user --requirement requirements.txt

Go to ``market_extraction_tool.py`` and replace:

> ``YOUR_API_KEY`` in the function ``import_web_intraday`` with your working AlphaVantage API key

> ``YOUR_API_KEY`` in the function ``import_web_daily`` with your working IEX API key

### How it works
The script will automatically extract the following tickers' data:
1. Oil & Gas: XOM, CVX, COP, EOG, OXY
2. Tech: AAPL, GOOGL, GOOG, FB, MSFT
3. Banking: JPM, BAC, C,WFC, GS
4. Recent IPOs: LYFT, PINS

with:

> main.py

You can run the script using command line arguments:

> main.py [--concurrent] [--replace] ``company tickers``

1. ``--concurrent`` will enable concurrent processes to download multiple tickers' data in parallel
2. ``--replace`` will replace the default list of companies to extract with the ticker(s) you included as command line argument(s)

As the scripts ends, it will plot the past 5 days intraday market data of Goldman Sachs (ticker: GS)