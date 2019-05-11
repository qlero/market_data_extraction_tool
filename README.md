Desc: Script that downloads intraday (past 5 days), daily (past 5 years) and active calls/puts of publicly traded companies.

Packages necessary to run the script: 

> arrow, matplotlib, numpy, pandas, pandas_datareader, requests, requests_html, yahoo_fin

Other packages that should be natively installed with python:

> arrow, datetime, json, os, multiprocessing, time

The companies covered are hardcoded as a list in the script. You can, of course, modify it.

As-is, the script will extract the following tickers' data:
1. Oil & Gas: XOM, CVX, COP, EOG, OXY
2. Tech: AAPL, GOOGL, GOOG, FB, MSFT
3. Banking: JPM, BAC, C,WFC, GS
4. Recent IPOs: LYFT, PINS

The script also contains a function to plot the past 5 days data of a single stock:

> single_company_to_analyze = "GS"

> short_term_analysis(single_company_to_analyze)

It is not active. You can activate it by removing the # in front of it.

Update on May 11th, 2019:
1. Clarification of all the comments in market_extraction_tool.py
2. Implementation of concurrency for a faster run
3. Update of the README.md to reflect changes