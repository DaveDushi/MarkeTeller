# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import os
import random
import openai
import requests
import time
import json
import logging
from filters import *
from pymongo import MongoClient
from flask_cors import CORS, cross_origin
from flask import Flask, send_from_directory, request, jsonify, redirect
from config import Config
from aiFunctions import *

ROOT_FOLDER = "./FrontEnd"
app = Flask(__name__, static_folder=os.path.join(ROOT_FOLDER, 'static'))
app.config.from_object(Config)
app.debug = True
cors = CORS(app)  # allows cors for our frontend

# logger setup
logger = logging.getLogger()
handler = logging.FileHandler('stockPriceService.log')
handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s : %(message)s'))
logger.addHandler(handler)
logger.setLevel(logging.INFO)

API_KEY = app.config['API_KEY']
API_KEY_GPT = app.config['API_KEY_GPT']
URI = app.config['DATABASE_URI']
client = MongoClient(URI,
                     tls=True,
                     tlsAllowInvalidCertificates=True)

stock_project = client.get_database('stock_project')


def parse_json(url):
    response = requests.get(url)
    return response.json()


@app.route('/')
def index():
    return 'Welcome to MarkeTeller!!'


@app.route('/search/<stock>')
def search(stock):
    api_key = app.config['API_KEY']
    search_query = request.args.get('stock')
    url = f'https://financialmodelingprep.com/api/v3/quote/{stock}?apikey={api_key}'
    response = requests.get(url)
    if len(response.json()) == 0:
        return "Stock Not Found"
    results = response.json()[0]
    data = {
        'Name': results['name'],
        'Symbol': results['symbol'],
        'Price': results['price'],
        'DayHigh': results['dayHigh'],
        'DayLow': results['dayLow']
    }
    return jsonify(data)


@app.route('/refresh')
def get_stock_list():
    stock_list = stock_project.get_collection('stock_list')

    # get the url that pulls a list of all tradeable stocks
    stocks_url = f'https://financialmodelingprep.com/api/v3/available-traded/list?apikey={API_KEY}'

    all_stocks = parse_json(stocks_url)
    # filter the list
    stocks_filtered = filter_stocks(all_stocks)

    stock_list.delete_many({})  # clear the old list

    # stock_list.insert_many(filtered_stocks)  # add the list to the database
    # pull more info for the filtered stocks
    symbol_list = [doc['symbol'] for doc in stocks_filtered]
    # add the stocks to the db 1500 at a time
    n = len(symbol_list)
    for i in range(0, n, 1500):
        if i + 1500 <= n:
            symbol_str = ','.join(symbol_list[i: i + 1500])
        else:
            symbol_str = ','.join(symbol_list[i:n])

        updated_url = f'https://financialmodelingprep.com/api/v3/quote/{symbol_str}?apikey={API_KEY}'
        updated_stocks = parse_json(updated_url)
        # get rid of the stocks that announced their earnings within a week or will announce
        updated_filtered = filter_updated(updated_stocks)

        # Select the fields name and symbol
        selected_fields = ['symbol', 'name']

        # Prepare the list of selected data
        selected_data_list = [{field: json_data[field] for field in selected_fields if field in json_data} for json_data
                              in updated_filtered]
        stock_list.insert_many(selected_data_list)  # add the symbols to the db

    return redirect('/refresh_rank')


@app.route('/refresh_rank')
def rank_stocks():
    # get the symbols from the db
    stock_list = stock_project.get_collection('stock_list')
    symbols = [doc['symbol'] for doc in stock_list.find()]

    # put them in a string to pull the batch from the api
    symbol_str = ','.join(symbols)
    url = f'https://financialmodelingprep.com/api/v3/quote/{symbol_str}?apikey={API_KEY}'
    stocks = parse_json(url)

    # Define weights for each factor
    weights = {
        "pe": 0.3,
        "eps": 0.2,
        "marketCap": 0.25,
        "changesPercentage": 0.1,
        "dayHigh": 0.05,
        "dayLow": 0.05,
        "priceAvg50": 0.025,
        "priceAvg200": 0.025,
    }

    def calculate_score(stock):
        score = 0
        for key, value in weights.items():
            if key in stock and stock[key] is not None:
                score += value * stock[key]
        return score

    ranked_stocks = sorted(stocks, key=calculate_score, reverse=True)

    ranked_list = [{"rank": rank, "name": stock['name'], "symbol": stock['symbol']} for rank, stock in
                   enumerate(ranked_stocks, start=1)]
    # add the list to the db
    ranked_stock_list = stock_project.get_collection('ranked_stock_list')
    ranked_stock_list.insert_many(ranked_stocks)
    return redirect('/rank')


@app.route('/rank')
def get_ranked():
    ranked_stock_list = stock_project.get_collection('ranked_stock_list')
    stocks = list(ranked_stock_list.find({}, {'_id': False}))
    return stocks[0:100]


@app.route('/my_stocks')
def user_stocks():
    my_stocks = stock_project.get_collection('my_stocks')
    stocks = list(my_stocks.find({}, {'_id': False}))

    return stocks


@app.route('/add/<symbol>')
def add_symbol(symbol):
    my_stocks = stock_project.get_collection('my_stocks')

    with app.test_request_context('/search', query_string={'stock': symbol}):
        response = search()
        response_data = response.get_json()
        filtered_data = {
            'Name': response_data['Name'],
            'Symbol': response_data['Symbol']
        }

    my_stocks.insert_one(filtered_data)

    return redirect('/my_stocks')


@app.route('/stock-pick')
def stock_pick():
    ranked_stock_list = stock_project.get_collection('ranked_stock_list')
    top_score = 0
    chosen_stock = ''
    numbers = random.sample(range(1, 101), 3)
    for x in numbers:
        stock = ranked_stock_list.find_one({'rank': x})['symbol']
        url = f'https://financialmodelingprep.com/api/v3/rating/{stock}?apikey={API_KEY}'
        rating = parse_json(url)[0]
        score_sum = (
                rating["ratingDetailsDCFScore"]
                + rating["ratingDetailsROEScore"]
                + rating["ratingDetailsROAScore"]
                + rating["ratingDetailsDEScore"]
                + rating["ratingDetailsPEScore"]
                + rating["ratingDetailsPBScore"]
        )
        if score_sum > top_score:
            top_score = score_sum
            chosen_stock = stock

    # Return the stock pick as JSON
    return redirect(f'/search/{chosen_stock}')


@app.route('/report/<stock>')
def generate_report(stock):
    report_db = stock_project.get_collection('report_db')
    upper_stock = stock.upper()
    report = list(report_db.find({'Symbol': upper_stock}, {'_id': False}))
    if report:
        return report[0]

    # set the api url's
    dividend_url = f"https://financialmodelingprep.com/api/v3/historical-price-full/stock_dividend/{stock}?limit=20&apikey={API_KEY}"
    income_url = f"https://financialmodelingprep.com/api/v3/income-statement/{stock}?apikey={API_KEY}"
    cash_flow_url = f"https://financialmodelingprep.com/api/v3/cash-flow-statement/{stock}?apikey={API_KEY}"
    balance_sheet_url = f"https://financialmodelingprep.com/api/v3/balance-sheet-statement/{stock}?apikey={API_KEY}"
    quote_url = f"https://financialmodelingprep.com/api/v3/quote/{stock}?apikey={API_KEY}"

    # pull the data
    dividend = parse_json(dividend_url)
    income_statement = parse_json(income_url)
    cash_flow = parse_json(cash_flow_url)
    balance_sheet = parse_json(balance_sheet_url)
    quote = parse_json(quote_url)

    # summarize the data
    summary = f"{summarize_text_with_chatgpt(json.dumps(dividend), 'dividend history', API_KEY_GPT)}\n" \
              f"{summarize_text_with_chatgpt(json.dumps(income_statement), 'income statement', API_KEY_GPT)}\n" \
              f"{summarize_text_with_chatgpt(json.dumps(cash_flow), 'cash flow statement', API_KEY_GPT)}\n" \
              f"{summarize_text_with_chatgpt(json.dumps(balance_sheet), 'balance sheet statement', API_KEY_GPT)}\n" \
              f"{summarize_text_with_chatgpt(json.dumps(quote), 'stock quote', API_KEY_GPT)}"

    # generate the report
    report = generate_financial_report(summary, API_KEY_GPT)

    data = {
        'Symbol': stock.upper(),
        'Report': report
    }
    # add the report to the DB
    result = report_db.insert_one(data)

    # Fetch the inserted document, exclude _id from the fields
    inserted_data = report_db.find_one({'_id': result.inserted_id}, {'_id': False})

    return jsonify(inserted_data)


if __name__ == '__main__':
    # main()
    # get_stock_list()
    app.run(host='0.0.0.0', port='81')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
