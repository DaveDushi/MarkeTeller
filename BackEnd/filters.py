import re
from datetime import timedelta, datetime


def filter_stocks(stocks):
    def should_filter(s):
        return filter_type(s['type']) or filter_exchange(s['exchangeShortName']) or filter_price(
            s['price']) or filter_name(s['name']) or filter_symbol(s['symbol'])

    def filter_type(s):
        return s in ['etf', 'trust']

    def filter_exchange(s):
        return s not in ["AMEX", "NASDAQ", "NYSE"]

    def filter_price(s):
        return s < 15

    def filter_name(s):
        return re.search('Water|Energy|Gas|Renewable|PLC|Utilities|Capital|Bank|Insurance', s)

    def filter_symbol(s):
        return re.search('\\.NS$|\\.BK$|-|JPM|HSBC|WFC|MS|GS|C|BLK', s)

    stocks = [s for s in stocks if not should_filter(s)]
    return stocks


def all_symbols(self):
    return


def filter_updated(updated_stocks):
    def should_filter(s):
        return filter_earning_an(s['earningsAnnouncement']) or filter_marketcap(s['marketCap'])

    def filter_earning_an(s):
        now = datetime.utcnow()
        last_week = now - timedelta(days=7)
        next_week = now + timedelta(days=7)
        return s is None or last_week <= datetime.fromisoformat(s[:-5]) <= next_week

    def filter_marketcap(s):
        return s < 2000000000

    updated_stocks = [s for s in updated_stocks if not should_filter(s)]
    return updated_stocks
