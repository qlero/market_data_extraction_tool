import market_data_extraction_tool as mdet
import argparse

def extraction(args, companies):
	"""
	Launches extraction(s).
	-----
	:param <args>: string ; arguments passed through the command line
	:param <companies>: list ; list of company tickers
	"""
	if len(args.firms) != 0:
		if args.replace:
			companies = args.firms
		else:
			companies.extend(args.firms)
	
	if args.concurrent:
		print("> Launch of concurrent extraction")
		mdet.main(companies, True)
		print("> Concurrent extraction performed")
	else:
		print("> Launch of linear extraction")
		mdet.main(companies, False)
		print("> Linear extraction performed")

# implementation of a command line parser
parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()
concurrent_parser = subparsers.add_parser("extraction")
concurrent_parser.add_argument("firms", type = str, nargs = "*", 
	help = "list of firm tickers to add to/or that replaces  the existing list stored in the <companies> variable.")
concurrent_parser.add_argument("--concurrent", action = "store_true", default = False,
	help = "Indicates the extraction is to be performed concurrently.")
concurrent_parser.add_argument("--replace", action = "store_true", default = False,
	help = "Indicates that the <firms> arguments will replace the existing list stored in the <companies> variable.")
concurrent_parser.set_defaults(func = extraction)

if __name__=='__main__':
	
	companies = ['XOM','CVX','COP','EOG','OXY','AAPL','GOOGL','GOOG','FB','MSFT','JPM','BAC','C','WFC','GS','LYFT','PINS']
	
	args = parser.parse_args()
	try:
		func = args.func
		func(args, companies)
	except AttributeError:
		print("> Too few arguments detected")
		print("> Defaulting to linear extraction")
		print("> Launch of linear extraction")
		mdet.main(companies, False)
		print("> Linear extraction performed")