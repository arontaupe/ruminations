import requests
import pandas as pd

HEADERS = ({'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})

asins = pd.read_csv('asins.csv')

for link in range(len(asins)):
    base_url = "https://www.amazon.com/"
    static = 'dp/'
    asin = asins.asin[0]
    url = base_url + static + asin
    html = requests.get(url, headers=HEADERS)
    if html.status_code != 404:
        print(url)
        print(html.status_code)
    else:
        print("-", end='')
