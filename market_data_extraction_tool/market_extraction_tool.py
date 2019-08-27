import arrow
import json
import os
import requests
import time

from multiprocessing import Process
from datetime import datetime
from yahoo_fin import options

import numpy as np
import pandas as pd
import pandas_datareader.data as web
import matplotlib.pyplot as plt
import matplotlib as mpl

# Register Pandas Formatters and Converters with matplotlib
# This function modifies the global matplotlib.units.registry dictionary
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

def import_web_intraday(ticker):
	"""
	Queries the website of the stock market data provider AlphaVantage (AV). AV provides stock, 
	forex, and cryptocurrency data. AV limits access for free users as such: 
		1. maximum of : 5 unique queries per minute, and 500 unique queries per 24h period
		2. Intraday history is capped at the past five days (current + 4)
		3. After-hour data is not available
	The provided data is JSON formatted. The data is a series of 'ticks' for each minute during 
	trading hours: open (09:30am) to closing (04:00pm). 
	Each tick lists the following stock data: open, close, low, high, average, volume
	--------
	:param <ticker>: String ; ticker of a company traded on the financial markets
	"""
	website = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol='+ticker+'&interval=1min&apikey=’+YOUR_API_KEY+’&outputsize=full&datatype=json'
	raw_json_intraday_data = requests.get(website)
	return raw_json_intraday_data.json()

def import_web_daily(ticker):
	"""
	Queries the API of the stock market data provider IEX. IEX provides stock, forex, 
	and cryptocurrency data. IEX limits access for free users as such:
		i. maximum of: 5 years of daily data (/!\ standard in finance is usually 10)
	The provided data is formatted as a panda dataframe.
	--------
	:param <ticker>: String ; ticker of a company traded on the financial markets
	"""
	end = datetime.today()
	start = end.replace(year=end.year-5)
	daily_data = web.DataReader(ticker, 'iex', start, end, access_key = "<YOURKEY>")
	return daily_data

def partition_save_intraday(ticker,json_extract):
	"""
	Saves a JSON array containing a company's intraday data in a folder named after 
	the company's ticker. It does:
		1. Creates a dictionary that contains the list of existing day date in the JSON
		array, formatted as "yyyy-mm-dd" as keys
		2. Splits the JSON array into separate JSON dictionaries (one for each covered day).
		Each created dictionary is saved as a single JSON file the folder mentioned above. 
		If a file shares the same name, both are merged:
			2.1 Checks if a directory named <ticker>\intraday_data exists
			2.2 Checks if a file named <ticker>_<date> in the directory. If so: merges 
			the created dictionary with the data stored in the existing file
			2.3 Saves the data (merged when applicable) in the folder under the name 
			<ticker>_<date>
	--------
	:param <ticker>: String ; ticker of a company traded on the financial markets
	:param <json_extract>: Dictionary ; JSON array of intraday data of company <ticker>
	"""
	# Step 1
	date = {}
	for item in json_extract: date[item[:10]] = "date"
	
	# Step 2
	for day in date.keys():
		daily_time_series = {}
		
		# Step 2.1
		for item in json_extract:
			if(item[:10] == day): daily_time_series[item] = json_extract[item]
		
		# Step 2.2
		path = ticker + "\\intraday_data"
		if(os.path.isdir(path) == False): os.makedirs(path)
		data_file_name = ticker + "_" + day
		
		# Step 2.3
		try:
			with open(os.path.join(path,data_file_name),'r') as file:
				existing_data_in_file = json.load(file)
				for item in existing_data_in_file:
					daily_time_series[item] = existing_data_in_file[item]
		
		except Exception as e:
			print(f"{ticker}: {e}")
		
		with open(os.path.join(path,data_file_name), 'w') as f:
			json.dump(daily_time_series, f)

def partition_save_daily(ticker, data_extract):
	"""
	Saves the retrieved dataframe in a folder named after the company's ticker. It does:
		1. Checks if a folder named <ticker> exists and creates it if not. Checks if a
		file named <ticker> exists in the folder. If so: merges the retrieved and existing
		data.
		2. Saves the data (merged when applicable) in the folder under the name <ticker>
	--------
	:param <ticker>: String ; ticker of a company traded on the financial markets
	:param <data_extract>: Dataframe ; Dataframe of daily data of company <ticker>
	"""
	# Step 1
	if(os.path.isdir(ticker) == False): os.mkdir(ticker)
	
	data_file_name = ticker
	data_extract_dictionary = data_extract.to_dict(orient="index")
	
	try:
		with open(os.path.join(ticker,data_file_name),'r') as file:
			existing_data_in_file = json.load(file)
			for item in existing_data_in_file: 
				data_extract_dictionary[item] = existing_data_in_file[item]
	
	except Exception as e:
		print(f"{ticker}: {e}")
	
	# Step 2
	with open(os.path.join(ticker,data_file_name), 'w') as f:
		json.dump(data_extract_dictionary, f)

def save_intraday(ticker):
	"""
	Saves AV's available intraday data for the company <ticker>.
	--------
	:param <ticker>: String ; ticker of a company traded on the financial markets
	"""
	raw_json = import_web_intraday(ticker)
	time_series_json = raw_json['Time Series (1min)']
	partition_save_intraday(ticker,time_series_json)

def save_daily(ticker):
	"""
	Saves IEX's available intraday data for the company <ticker>.
	--------
	:param <ticker>: String ; ticker of a company traded on the financial markets
	"""
	raw_dataframe = import_web_daily(ticker)
	partition_save_daily(ticker,raw_dataframe)

def extract_save_option_data(ticker):
	"""
	Imports and saves from the yahoo finance database a company's option data. 
	The option data is split per type (call or put), expiration date, and day.
	It does:
		1. Checks for nested directories:
			<ticker>\options_data_<ticker>\<expiration_date>_<ticker>_<options>
			Creates it if non-existent. 
		2. Checks in the folder for a file named:
			<expiration_date>_<ticker>_<calls/puts>_as-at_<date_extract> 
			If so: merges the existing and newly extracted data.
		3. Saves the data (merged when applicable) in the folder under the company's 
		ticker.
	--------
	:param <ticker>: String ; ticker of a company traded on the financial markets
	"""
	extract_dates = options.get_expiration_dates(ticker)
	today = datetime.today().strftime("%Y-%m-%d")
	
	for expiration_date in extract_dates:
		format_date = arrow.get(expiration_date, 'MMMM D, YYYY').format('YYYY-MM-DD')
		extract_date = arrow.get(expiration_date, 'MMMM D, YYYY').format('MM/DD/YYYY')
		
		try:
			extract = options.get_options_chain(ticker, extract_date)
			path = ticker + "\\options_data_" + ticker + "\\" + format_date + "_" + ticker + "_options"
			option_types = ["calls", "puts"]
			
			for option in option_types:
				extract_chain = extract[option]
				extract_chain = extract_chain.to_dict(orient="index")
				data_file_name = format_date + "_" + ticker + "_" + option + "_as-at_" + today
				
				# Step 1
				if not os.path.exists(path): os.makedirs(path)
				
				# Step 2
				if os.path.isfile(os.path.join(path,data_file_name)) == True:
					try:
						with open(os.path.join(path,data_file_name),'r') as file:
							existing_data_in_file = json.load(file)
							for item in existing_data_in_file:
								extract_chain[item] = existing_data_in_file[item]
					
					except Exception as e:
						print(f"{ticker}: {e}")
				
				#Step 3
				with open(os.path.join(path,data_file_name), 'w') as f:
					json.dump(extract_chain, f)
					print(f"{ticker}: {format_date} {option} options data retrieved successfully!\n")
		
		except Exception as e:
			print(f"{ticker}: {format_date} options data could not be retrieved.\n")

def extract_info_intraday(company_list):
	"""
	Calls the extract and save functions above for each input company.
	--------
	:param <company_list>: List ; list of publicly traded companies' tickers
	"""
	try:
		for company in company_list:
			save_intraday(company)
			print(f"{company}: intraday market data retrieved successfully!\n")
			if ((company_list.index(company)+1) % 5 == 0 and company_list.index(company)+1 != len(company_list)):
				print("ALPHAVANTAGE REQUEST LIMIT REACHED - WAITING FOR 1 MINUTE\n")
				time.sleep(60)
				print("1 MINUTE PASSED - RETURN TO REQUESTING ALPHAVANTAGE\n")
	
	except Exception as e:
		print(f"{company}: {e}")

def extract_info_daily_and_options(company_list):
	"""
	Calls the extract and save functions above for each input company.
	--------
	:param <company_list>: List ; list of publicly traded companies' tickers
	"""
	try:
		for company in company_list:
			if ((company_list.index(company)+1) % 10 == 0 and company_list.index(company)+1 != len(company_list)):
				print("YAHOO FINANCE REQUEST LIMIT REACHED - WAITING FOR 1 MINUTE\n")
				time.sleep(60)
				print("1 MINUTE PASSED - RETURN TO REQUESTING YAHOO FINANCE\n")
			save_daily(company)
			print(f"{company} daily market data retrieved successfully!\n")
			extract_save_option_data(company)
	except Exception as e:
		print(f"{company}: {e}")

def extract_info_all(company_list):
	"""
	Calls the extract and save functions above for each input company.
	--------
	:param <company_list>: List ; list of publicly traded companies' tickers
	"""
	try:
		for company in company_list:
			save_intraday(company)
			print(f"{company} intraday market data retrieved successfully!\n")
			save_daily(company)
			print(f"{company} daily market data retrieved successfully!\n")
			extract_save_option_data(company)
			if ((company_list.index(company)+1) % 5 == 0 and company_list.index(company)+1 != len(company_list)):
				print("ALPHAVANTAGE REQUEST LIMIT REACHED - WAITING FOR 1 MINUTE\n")
				time.sleep(60)
				print("1 MINUTE PASSED - RETURN TO REQUESTING ALPHAVANTAGE\n")
				
	except Exception as e:
		print(f"{company}:{e}")

def short_term_analysis(ticker):
	"""
	Extracts intraday data of a single company from AV's website or from an existing
	local file. It does:
	1. Checks if data for the company exists locally. If so: retrieves it. If not:
	requests it from AV's website. The data is extracted as a JSON array and formatted
	as a DataFrame.
	2. Formats the dataframe to fit the following format:
			DATE (index)| MARKET DATA
			date 1		| open | low | high | etc.
			date 2		| open | low | high | etc.
			etc. 		| etc.
		2.1 Modifies the type of each instance of the MARKET DATA from a string to 
		a float.
		2.2 Creates an empty set of each single day covered in the data formatted as
		"yyyy-mm-dd".
		2.3 Modifies the type of each instance of the DATE (index) from a string or 
		integer to a datetime.
		2.4 Formats the data into an array to be plotted. FYI, The minute data provided by
		AV runs from 09:31:00am to 04:00:00pm. The opening bell tick (09:30:00am) is 
		missing. AV's data is actually lagged by a minute, i.e. the opening value of a 
		stock at 09:30:00am corresponds to the “1. open” value linked to the index 
		"09:31:00am". The actual daily data per minute of a stock can be approximated 
		as such: “1. open” 09:31:00am datum + “4. close” 09:31:00am to 04:00:00pm data.
	3. Plots the data
	--------
	:param <ticker>: String ; ticker of a company traded on the financial markets
	"""
	# Step 1
	path = ticker + "\\intraday_data"
	market_data = {}
	try:
		covered_date_filenames = os.listdir(path)[-5:]
		for filename in covered_date_filenames:
			with open(os.path.join(ticker,"intraday_data",filename),'r') as file:
				load_dict = json.load(file)
			market_data = {**market_data, **load_dict}
		market_data_minute_time_series = pd.DataFrame(market_data).transpose()
		print("Data loaded from existing local file.")
	except Exception as e:
		print(f"{ticker}: {e}")
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
	for counter, index in enumerate(market_data_minute_time_series.index):
		if str(index)[-8:] == "09:31:00" and str(market_data_minute_time_series.iloc[counter-1])[-8:] != "09:30:00":
			market_data_minute_time_series.loc[pd.Timestamp(str(index)[:11]+"09:30:00")] = [0,0,0,market_data_minute_time_series.iloc[counter][0],0]
	market_data_minute_time_series = market_data_minute_time_series.sort_index()
	
	# Step 3
	plt.style.use('ggplot')
	fig, ax = plt.subplots(1, len(dates_in_time_series), figsize=(16,7))
	plt.suptitle(ticker, size = 20, y=0.93)
	i = 0
	for counter, (group_name, df_group) in enumerate(market_data_minute_time_series.groupby(pd.Grouper(freq='D'))):
		if df_group.empty == False:
			ax[counter-i].plot(df_group['4. close'], color = "blue")
			xfmt = mpl.dates.DateFormatter('%m-%d %H:%M')
			ax[counter-i].xaxis.set_major_locator(mpl.dates.MinuteLocator(byminute=[30], interval = 1))
			ax[counter-i].xaxis.set_major_formatter(xfmt)
			ax[counter-i].get_xaxis().set_tick_params(which='major', pad=4)
			ax[counter-i].set_ylim(min(market_data_minute_time_series['4. close'])-
				round(0.005*min(market_data_minute_time_series['4. close']),0),
				max(market_data_minute_time_series['4. close'])+
				round(0.005*max(market_data_minute_time_series['4. close']),0))
		else:
			i += 1
		fig.autofmt_xdate()
	plt.show()

def main(company_list):
	"""
	Main function call.
	--------
	:param <company_list>: List ; list of publicly traded companies' tickers
	"""
	# Oil & Gas: XOM, CVX, COP, EOG, OXY
	# Tech: AAPL, GOOGL, GOOG, FB, MSFT
	# Banking: JPM, BAC, C,WFC, GS
	# Recent IPO: LYFT, PINS

	#Concurrent running
	#try:
	#	process_1 = Process(target = extract_info_intraday, args=(company_list,))
	#	process_1.start()
	#	process_2 = Process(target = extract_info_daily_and_options, args=(company_list,))
	#	process_2.start()
	#except Exception as e:
	#	print(e)
	
	#Sequential running
	extract_info_intraday(company_list)
	extract_info_daily_and_options(company_list)
	#extract_info_all(company_list)

	single_company_to_analyze = "GS"
	short_term_analysis(single_company_to_analyze)





