import market_data_extraction_tool as mdet
import sys

if __name__=='__main__':
	
	firms = ['XOM','CVX','COP','EOG','OXY','AAPL','GOOGL','GOOG','FB','MSFT','JPM','BAC','C','WFC','GS','LYFT','PINS']
	
	#checks if the script was run with command line arguments
	if len(sys.argv) > 1:
		print (f"the script has the name {sys.argv[0]}.")
		print (f"the script is called with {len(sys.argv)-1} arguments.")
	
	list_argv = [arg for arg in sys.argv[1:]]
	
	if ("True" in list_argv) and ("False" not in list_argv): 
		print("--Extraction performed concurrently--")
		mdet.main(firms, True)
	else:
		print("--Extraction performed linearly--")
		mdet.main(firms)