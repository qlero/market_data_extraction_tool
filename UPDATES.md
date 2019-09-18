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

Update on September 12th, 2019:
1. Implemented a command line parameter pull so users can choose to extract data concurrently or not in the command line:

> $main.py True

"True" is case sensitive.

Update on September 17th, 2019:
1. Add argparse
2. Review of README.md
3. inclusion of requirements.txt