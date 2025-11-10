import sys

def get_key(dictionary, value):
    for k, v in dictionary.items():
        if v == value:
            return k

def all_stocks(data):
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
    if check_commas(data):
        args_list = data.split(',')
        if (len(' '.join(args_list).split()) == len(args_list) and len(args_list) <= 11):
            for arg in args_list:
                arg = ''.join(c for c in arg if c.isalnum())
                if arg.capitalize() in COMPANIES.keys():
                    print(f'{arg.capitalize()} stock price is {STOCKS[COMPANIES[arg.capitalize()]]}')
                elif arg.upper() in STOCKS.keys():
                    print(f'{arg.upper()} is a ticker symbol for {get_key(COMPANIES, arg.upper())}')
                else:
                    print(f'{arg} is an unknown company or an unknown ticker symbol')

def check_commas(data):
    is_comma = i = 0
    res = True
    while res and i < len(data):
        if data[i] == ',':
            is_comma += 1
        elif data[i] != " ":
            is_comma = 0
        if is_comma > 1:
            res = False
        i += 1
    return res
    

if __name__ == '__main__':
    if len(sys.argv) > 1 and len(sys.argv) <= 12:
        data = ""
        for i in range(1, len(sys.argv)):
            data += sys.argv[i] + " "
        all_stocks(data)
