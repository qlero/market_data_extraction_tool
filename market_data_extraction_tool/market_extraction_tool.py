#!/usr/bin/env python
# coding: utf-8
# To install: requests, numpy, pandas, pandas_datareader, matplotlib, yahoo_fin, arrow, requests_html

import os
import json
import requests
import requests_html
import time
import arrow

from datetime import datetime
from yahoo_fin import options

import numpy as np
import pandas as pd
import pandas_datareader.data as web
import matplotlib.pyplot as plt
import matplotlib as mpl

#Register Pandas Formatters and Converters with matplotlib
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

def change_working_directory():
	"""
	change_working_directory inputs the user to know whether they want to change their
	current working directory. If yes, the function will create a "Market Data Extract"
	folder on the user's desktop where the data will be stored.
	"""	
	while True:
		value = input("Do you wish to change the working directory to your desktop? (Y/N): ")
		if (value == "Y" or value == "N"):
			break
	if value == "Y":
		current_directory = os.getcwd()
		temporary_directory = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop') + "//Market Data Extract"
		if(os.path.isdir(temporary_directory) == False):
			os.makedirs(temporary_directory)
			print("The path " + temporary_directory + " was created.")
		new_directory = os.chdir(temporary_directory)
		print("You swapped from the working directory " + str(current_directory) + " to " + str(os.getcwd()))
	else:
		print("Your current directory remains " + str(os.getcwd()) + ".")

def import_web_intraday(ticker):
    """
    import_web_intraday() is a function that takes one argument <ticker>.
    The function queries the website and stock market data provider AlphaVantage.
    AlphaVantage provides stocks, forex and cryptocurrencies data. Please be aware
    of AlphaVantage’s limits for free users:
    - maximum of 5 unique queries per minute
    - maximum of 500 unique queries per 24h period
    - History is capped at the current day and the past 4 days for intraday stock data
    - After-hour data is not available
    The requested data is the stock data of the company with ticker <ticker>, and is
    provided as a JSON. It covers the daily trading at a minute frequency from open
    (09:30am) to closing (04:00pm) bell. The data provided for each minute is as follow:
    open, close, low, high, average, and volume.
    """
    website = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol='+ticker+'&interval=1min&apikey=’+YOUR_API_KEY+’&outputsize=full&datatype=json'
    raw_json_intraday_data = requests.get(website)
    return raw_json_intraday_data.json()

def import_web_daily(ticker):
	"""
	import_web_daily() is a function that takes one argument <ticker>. The 
	function the stock market data provider IEX. The IEX provides stocks, forex 
	and cryptocurrencies data. Please be aware of IEX’s limits for free users:
	- History is capped to a maximum of 5 years*
	The requested data is the stock data of the company with ticker <ticker>, and 
	is provided as a panda dataframe.
	*The preferred standard for history analysis in Finance is usually 10 years.
	"""
	end = datetime.today()
	start = end.replace(year=end.year-5)
	daily_data = web.DataReader(ticker, 'iex', start, end)
	return daily_data

def partition_save_intraday(json_extract,ticker):
    """
    partition_save_intraday() is a function that takes two arguments <json_extract>,
    <ticker>. It saves the json data <json_extract> in a folder named after the 
    ticker <ticker> of the target company. As-is, it saves the data retrieved while 
    calling the function import_web_intraday(). It proceeds as such:
        1. Creates an empty dictionary <date> and stores in it each day covered by 
        <json_extract>. Each unique day is stored under the format "yyyy-mm-dd". 
        2. Splits the <json_extract> into separate json dictionaries by each unique 
        day date stored in <date>. Each dictionary is saved as a singular JSON file 
        named <ticker>_<date> in an existing or newly created folder named <ticker>. 
        If such a file already exists, the function merges both.
            2.1 Checks for a directory named <ticker>\intraday_data exists
            2.2 Checks for a file named <ticker>_<date> in the directory. If so, the 
            function merges the split data with the data stored in the existing file
            2.3 Saves the data (merged when applicable) in the folder under the name 
            <ticker>_<date>
    """    
    # Step 1
    date = {}
    for item in json_extract:
        date[item[:10]] = "date"
    # Step 2
    for day in date.keys():
        daily_time_series = {}
        # Step 2.1
        for item in json_extract:
            if(item[:10] == day):
                daily_time_series[item] = json_extract[item]
        # Step 2.2
        path = ticker + "\\intraday_data"
        if(os.path.isdir(path) == False):
            os.makedirs(path)
        data_file_name = ticker + "_" + day
        # Step 2.3
        try:
            with open(os.path.join(path,data_file_name),'r') as file:
                existing_data_in_file = json.load(file)
                for item in existing_data_in_file:
                    daily_time_series[item] = existing_data_in_file[item]
        except Exception as e:
            pass
        with open(os.path.join(path,data_file_name), 'w') as f:
            json.dump(daily_time_series, f)
    pass

def partition_save_daily(data_extract, ticker):
    """
    partition_save_daily() is a function that takes two arguments <data_extract>,
    <ticker>. It saves the data <data_extract> in a folder named after the ticker
    <ticker> of the target company. As-is, it saves the data retrieved while calling
    the function import_web_daily(). It proceeds as such:
        1. Checks for folder named <ticker> and creates it if non-existent. Checks 
        for a file named <ticker> in the folder. If so, the function merges the 
        split data with the data stored in the existing file.
        2. Saves the data (merged when applicable) in the folder under the name 
        <ticker>
    """
    # Step 1
    if(os.path.isdir(ticker) == False):
        os.mkdir(ticker)
    data_file_name = ticker
    data_extract_dictionary = data_extract.to_dict(orient="index")
    try:
        with open(os.path.join(ticker,data_file_name),'r') as file:
            existing_data_in_file = json.load(file)
            for item in existing_data_in_file:
                data_extract_dictionary[item] = existing_data_in_file[item]
    except Exception as e:
        pass
    # Step 2
    with open(os.path.join(ticker,data_file_name), 'w') as f:
        json.dump(data_extract_dictionary, f)
    pass

def save_intraday(ticker):
    """
    save_intraday() is a function that takes one argument <ticker>. It calls 
    import_web_intraday() and partition_save_intraday() to extract and save 
    the available AlphaVantage's market data for the company with the ticker 
    <ticker>. The save is performed in the same folder as that of the script 
    calling this function.
    """
    raw_json = import_web_intraday(ticker)
    time_series_json = raw_json['Time Series (1min)']
    partition_save_intraday(time_series_json,ticker)
    pass

def save_daily(ticker):
    """
    save_daily() is a function that takes one argument <ticker>. It calls 
    import_web_daily() and partition_save_daily() to extract and save the 
    available IEX’s market data for the company with the ticker <ticker>. 
    The save is performed in the same folder as that of the script calling 
    this function.
    """
    raw_json = import_web_daily(ticker)
    partition_save_daily(raw_json,ticker)
    pass

def extract_save_option_data(ticker):
	"""
	extract_save_option_data is a function that takes one argument <ticker>. It
	imports option data from the company with the ticker <ticker> from the yahoo
	finance database online.
	The save is performed in the same folder as that of the script calling 
    this function. The option data is saved per day and splits calls and puts in
	two different files. It proceeds as such:
        1. Checks for nested directories <ticker>\options_data_<ticker>\<expiration_date>_<ticker>_<options>
		and creates it if non-existent. Checks for a file named <expiration_date>_<ticker>_<calls/puts>_as-at_<date_extract> 
		in the folder. If so, the function merges the existing data with data newly extracted.
        2. Saves the data (merged when applicable) in the folder under the name 
        <ticker>
	"""
	extract_dates = options.get_expiration_dates(ticker)
	today = datetime.today().strftime("%Y-%m-%d")
	for expiration_date in extract_dates:
		extract = options.get_options_chain(ticker)
		format_date = arrow.get(expiration_date, 'MMMM D, YYYY').format('YYYY-MM-DD')
		print("Attempting to retrieve " + ticker + " " + format_date + " active call and put options data.")
		# Step 1
		if not os.path.exists(str(ticker + "\\options_data_" + ticker + "\\" + format_date + "_" + ticker + "_options")):
			os.makedirs(str(ticker + "\\options_data_" + ticker + "\\" + format_date + "_" + ticker + "_options"))
		try:
			with open(os.path.join(str(ticker + "\\options_data_" + ticker + "\\" + format_date + "_" + ticker + "_options"),format_date + "_" + ticker + "_calls_as-at_" + today),'r') as file:
				existing_data_in_file = json.load(file)
				for item in existing_data_in_file:
					extract["calls"][item] = existing_data_in_file[item]
			with open(os.path.join(str(ticker + "\\options_data_" + ticker + "\\" + format_date + "_" + ticker + "_options"),format_date + "" + ticker + "_puts_as-at_" + today),'r') as file:
				existing_data_in_file = json.load(file)
				for item in existing_data_in_file:
					extract["puts"][item] = existing_data_in_file[item]
		except Exception as e:
			pass
		# Step 2
		with open(os.path.join(str(ticker + "\\options_data_" + ticker + "\\" + format_date + "_" + ticker + "_options"),format_date + "_" + ticker + "_calls_as-at_" + today), 'w') as f:
			json.dump(extract["calls"].to_dict(orient="index"), f)
			print(format_date + " call options for " + ticker + " retrieved successfully!")
		with open(os.path.join(str(ticker + "\\options_data_" + ticker + "\\" + format_date + "_" + ticker + "_options"),format_date + "_" + ticker + "_puts_as-at_" + today), 'w') as f:
			json.dump(extract["puts"].to_dict(orient="index"), f)
			print(format_date + " put options for " + ticker + " retrieved successfully!")
	pass

def extract_info(company_list):
	"""
	extract_info() is a function that takes one list argument < company_list>. It 
	calls save_intraday() and save_daily() to extract and save the intraday and 
	daily market data intraday market data for each ticker in the list <company_list>.
	"""
	#/!\ implement multi-processing for optimized extraction
	try:
		for company in company_list:
			print("Attempting to retrieve " + company + " intraday market data.")
			save_intraday(company)
			print(company + " intraday market data retrieved successfully!")
			print("Attempting to retrieve " + company + " daily market data.")
			save_daily(company)
			print(company + " daily market data retrieved successfully!")
			extract_save_option_data(company)
			if ((company_list.index(company)+1) % 5 == 0 and company_list.index(company)+1 != len(company_list)):
				print("Waiting 1 minute for AlphaVantage refresh.")
				time.sleep(60)
	except Exception as e:
		print(e)
		pass

def short_term_analysis(ticker):
    """
    short_term_analysis() is a function that takes one string argument <ticker>.
    It extracts the intraday market data of one single company whose ticker is
    <ticker> from either the online data provided by AlphaVantage, or the data
    already existing locally. It calls import_web_intraday() to retrieve the AlphaVantage 
    data if necessary. It proceeds as such:
        1. Checks if data for the company <ticker> exists locally and retrieves it, 
        either by extracting it from a local file or from AlphaVantage’s api. The data, 
        extracted as JSON, is reformatted as a DataFrame.
        2. Reformats the data to be plotable. The final formatting should be as such:
        DATE | MARKET DATA
        Index date 1 | open, low, high, etc. of 1
        Index date 2 | open, low, high, etc. of 2
        etc. | etc.
        2.1 Modifies the data type of each datum in each column from a string to a float
        2.2 Creates an empty set of each single date day covered in the data. Each unique 
        day is stored under the format "yyyy-mm-dd".
        2.3 Modifies the type of the dataframe index from a string or integer to a datetime
        2.4 Creates the list of data to be plotted. The minute data provided by AlphaVantage
        runs from 09:31:00am to 04:00:00pm. It technically misses the starting point 09:30:00am,
        so called open bell in Finance. AlphaVantage's data is delayed by a minute. I.e. the 
        opening value of a stock at 09:30:00am corresponds to the 09:31:00 “1. open” value of 
        the index 09:31:00am. The actual daily data per minute of a stock can be approximated 
        as such: “1. open” 09:31:00am datum + “4. close” 09:31:00am to 04:00:00pm data.
        3. Plots the data
    """   
    # Step 1
    path = ticker + "\\intraday_data"
    covered_date_filenames = os.listdir(path)[-5:]
    market_data = {}
    try:
        for filename in covered_date_filenames:
            with open(os.path.join(ticker,"intraday_data",filename),'r') as file:
                load_dict = json.load(file)
            market_data = {**market_data, **load_dict}
        market_data_minute_time_series = pd.DataFrame(market_data).transpose()
        print("Data loaded from existing local file.")
    except Exception as e:
        market_data = import_web_intraday(ticker)
        market_data_minute_time_series = pd.DataFrame(market_data["Time Series (1min)"]).transpose()
        market_data_minute_time_series = market_data_minute_time_series.reindex(index=market_data_minute_time_series.index[::-1])
        print("Data loaded from data repository online.")    
    # Step 2
    # Step 2.1
    for column in market_data_minute_time_series.keys():
        market_data_minute_time_series[column] = market_data_minute_time_series[column].astype('float64')     
    # Step 2.2 
    dates_in_time_series = sorted(set([x[:10] for x in market_data_minute_time_series.index.tolist()]))
    # Step 2.3
    market_data_minute_time_series.index = pd.to_datetime(market_data_minute_time_series.index, format = '%Y-%m-%d %H:%M:%S')
    # Step 2.4
    i = 0
    for index in market_data_minute_time_series.index:
        if str(index)[-8:] == "09:31:00" and str(market_data_minute_time_series.iloc[i-1])[-8:] != "09:30:00":
            market_data_minute_time_series.loc[pd.Timestamp(str(index)[:11]+"09:30:00")] = [0,0,0,market_data_minute_time_series.iloc[i][0],0]
        i += 1
    market_data_minute_time_series = market_data_minute_time_series.sort_index()
    # Step 3
    plt.style.use('ggplot')
    fig, ax = plt.subplots(1, len(dates_in_time_series), figsize=(16,7))
    plt.suptitle(ticker, size = 20, y=0.93)
    i = 0
    for group_name, df_group in market_data_minute_time_series.groupby(pd.Grouper(freq='D')):
        if df_group.empty == False:
            ax[i].plot(df_group['4. close'], color = "blue")
            xfmt = mpl.dates.DateFormatter('%m-%d %H:%M')
            ax[i].xaxis.set_major_locator(mpl.dates.MinuteLocator(byminute=[30], interval = 1))
            ax[i].xaxis.set_major_formatter(xfmt)
            ax[i].get_xaxis().set_tick_params(which='major', pad=4)
            ax[i].set_ylim(min(market_data_minute_time_series['4. close'])-
                           round(0.005*min(market_data_minute_time_series['4. close']),0),
                           max(market_data_minute_time_series['4. close'])+
                           round(0.005*max(market_data_minute_time_series['4. close']),0))
            fig.autofmt_xdate()
            i += 1
    plt.show()

# Oil & Gas: XOM, CVX, COP, EOG, OXY
# Tech: AAPL, GOOGL, GOOG, FB, MSFT
# Banking: JPM, BAC, C,WFC, GS
# Recent IPO: LYFT, PINS
companies = ['XOM','CVX','COP','EOG','OXY','AAPL','GOOGL','GOOG','FB',"MSFT",'JPM','BAC','C','WFC','GS','LYFT',"PINS"]

change_working_directory()
extract_info(companies)

#single_company_to_analyze = "GS"
#short_term_analysis(single_company_to_analyze)




