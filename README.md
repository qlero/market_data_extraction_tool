Description: Script that downloads intraday (past 5 days), daily (past 5 years) and active calls/puts of publicly traded companies.

The companies covered are hardcoded as a list in the script. You can, of course, modify it.
As-is, the script will extract the following tickers' data:
Oil & Gas: XOM, CVX, COP, EOG, OXY
Tech: AAPL, GOOGL, GOOG, FB, MSFT
Banking: JPM, BAC, C,WFC, GS
Recent IPOs: LYFT, PINS

Packages necessary to run the script: arrow, matplotlib, numpy, pandas, pandas_datareader, requests, requests_html, yahoo_fin
