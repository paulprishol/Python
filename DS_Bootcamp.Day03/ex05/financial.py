import sys
import requests
from bs4 import BeautifulSoup

def get_info(ticker, field):
    session = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "Referer": "https://finance.yahoo.com/",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
    }
    session.get("https://finance.yahoo.com/", headers=headers)
    url = f'https://finance.yahoo.com/quote/{ticker}/financials/?p={ticker.lower()}'
    response = session.get(url, headers=headers)
    if response.status_code == 200:
        if response.url == url:
            soup = BeautifulSoup(response.text, 'html.parser')
            table = soup.find('div', class_='tableBody')
            row = table.find(class_='rowTitle', title=field)
            rows = row.find_parent(class_='row')
            values = rows.find_all(class_='column')
            return tuple(value.text.strip() for value in values)
        else:
            raise ValueError(f'Incorrect url: current is {response.url}')
    else:
        raise ConnectionError(f'Error: {response.status_code}')

if __name__ == '__main__':
    try:
        if len(sys.argv) == 3:
            ticker = sys.argv[1]
            field = sys.argv[2]
            print(get_info(ticker, field))
        else:
            raise Exception
    except (ValueError, ConnectionError) as e:
        print(e)
    except AttributeError:
        print('Incorrect field name')
    except Exception:
        print('Error: Incorrect amount of arguments')