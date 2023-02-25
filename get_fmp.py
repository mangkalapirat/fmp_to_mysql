import json
import requests
import os
from dotenv import load_dotenv

from utils import db

def insert_data(table_name, data_list):
    db_connection = db.get_connection()

    ### Prepare data to insert
    cols = []
    vals = []
    for data_row in data_list:
        if cols==[]:
            cols = list(data_row.keys())
        vals_replace_empty = [None if val=="" else val for val in list(data_row.values())]
        vals.append( vals_replace_empty )
    cursor = db_connection.cursor()
    ### Prepare Statement for insert data
    insert_sql = f'REPLACE INTO {table_name} ({",".join(cols)}) VALUES( %s {", %s"* (len(cols)-1)})'
    ### Execute Insert Statement
    cursor.executemany(insert_sql, vals)
    db_connection.commit()
    db_connection.close()

def get_api_data(url):
    ### Get data from API then return data as dictionary
    response = requests.get(url)
    if response.status_code==200:
        return json.loads(response.text)

if __name__=='__main__':
    load_dotenv()
    api_key = os.environ.get('api_key')

    ### Create tables
    db.init_tables()

    ### Loop to get historical dividends data for each symbols in list
    symbol_list = ['AAPL', 'WBA']
    for symbol in symbol_list:
        ### Get Historical Dividends data from API
        hist_div_data = get_api_data(f'https://financialmodelingprep.com/api/v3/historical-price-full/stock_dividend/{symbol}?apikey={api_key}')
        historical_list = hist_div_data['historical']
        for hist in historical_list:
            hist['symbol'] = symbol
        
        ### Insert data into table
        insert_data('historical_dividends', historical_list)


    ### Get delisted companies data from API
    delisted_comp_data = get_api_data(f'https://financialmodelingprep.com/api/v3/delisted-companies?page=0&apikey={api_key}')

    ### Insert data into table
    insert_data('delisted_companies', delisted_comp_data)

