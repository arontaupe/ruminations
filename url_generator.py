import requests
import pandas as pd

def gen_url(attribute):

    df = pd.read_csv('amazon_scrapy/amazon_scrapy/spiders/crawl_results.csv')
    subdf = df[df['query'].str.contains(attribute)]
    urllist = []
    for index, row in subdf.iterrows():
        base_url = "https://www.amazon.com/"
        static = 'dp/'
        asin = row.asin
        url = base_url + static + asin
        html = requests.get(url)
        if html.status_code != 404:
            #print(url, end=' ')
            urllist.append(url)
    #print("")
    #print(urllist)
    return urllist
