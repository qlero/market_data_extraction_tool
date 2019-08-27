# market_data_extraction_tool
market_data_extraction_tool is a script that downloads:
- intraday (past 5 days)
- daily (past 5 years)
- active calls/puts of publicly traded companies.

### Installation
market_data_extraction_tool requires Python 3.x to run. It uses the following modules:
> arrow, datetime, json, os, matplotlib, multiprocessing, numpy, pandas, pandas_datareader, requests, time, yahoo_fin

### How it works
As-is, the script will extract the following tickers' data:
1. Oil & Gas: XOM, CVX, COP, EOG, OXY
2. Tech: AAPL, GOOGL, GOOG, FB, MSFT
3. Banking: JPM, BAC, C,WFC, GS
4. Recent IPOs: LYFT, PINS

Please provide your IEX API token in the function import_web_daily()

The companies covered are hardcoded as a list in the script. You can, of course, modify it.

The script also contains a function to plot the past 5 days data of a single stock:
> single_company_to_analyze = "GS"

> short_term_analysis(single_company_to_analyze)

### Past Updates
Update on May 11th, 2019:
1. Clarified each comments in market_extraction_tool.py
2. Implemented concurrency for a faster run
3. Updated the README.md to reflect changes

Update on June 3rd, 2019:
1. Patched the short_term_analysis() function: It would crash when searching for an folder containing intraday data that does not exist
2. Clarified/simplified the error messaging when the program checks for unexisting folders
3. Patched the extraction of Option data: Yahoo seems to throttle requests, added a time.sleep(60) after 10 company requests
4. Updated the README.md to reflect changes

Update on June 4th, 2019:
1. Clarified/simplified the error messaging when the program fails to request option data
2. Updated ongoing issues
3. Updated the README.md to reflect changes

Update on August 24th, 2019:
1. Updated the code for readability
2. The IEX data provider now requires an API token to work

Update on August 28th, 2019:
1. Updated the code structure