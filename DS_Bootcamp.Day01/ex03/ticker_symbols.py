import sys

def get_key(dictionary, value):
    for k, v in dictionary.items():
        if v == value:
            return k

def price_check(data):
    COMPANIES = {
        'Apple': 'AAPL',
        'Microsoft': 'MSFT',
        'Netflix': 'NFLX',
        'Tesla': 'TSLA',
        'Nokia': 'NOK'
    }

    STOCKS = {
        'AAPL': 287.73,
        'MSFT': 173.79,
        'NFLX': 416.90,
        'TSLA': 724.88,
        'NOK': 3.37
    }
    
    ticker = data.upper()
    if ticker in STOCKS.keys():
        print(f'{get_key(COMPANIES, ticker)} {STOCKS[ticker]}')
    else:
        print("Unknown ticker")


if __name__ == '__main__':
    if len(sys.argv) == 2:
        price_check(sys.argv[1])

