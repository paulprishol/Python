import sys

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
    
    companies_list = [i.lower() for i in COMPANIES.keys()]
    company = data.lower()
    if company in companies_list:
        print(STOCKS[COMPANIES[company.capitalize()]])
    else:
        print("Unknown company")


if __name__ == '__main__':
    if len(sys.argv) == 2:
        price_check(sys.argv[1])

