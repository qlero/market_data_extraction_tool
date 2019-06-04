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
1. Clarified each comments in market_extraction_tool.py
2. Implemented concurrency for a faster run
3. Updated the README.md to reflect changes

Update on June 3rd, 2019:
1. Patched the short_term_analysis() function: It would crash when searching for an folder containing intraday data that does not exist
2. Clarified/simplified the error messaging when the program checks for unexisting folders
3. Patched the extraction of Option data: Yahoo seems to throttle requests, added a time.sleep(60) after 10 company requests
4. Updated the README.md to reflect changes