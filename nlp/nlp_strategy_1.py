import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os



seed_urls = ['https://inshorts.com/en/read/technology',
             'https://inshorts.com/en/read/sports',
             'https://inshorts.com/en/read/world']

def build_dataset(seed_urls):
    new_data = []
    for url in seed_urls:
        news_category = url.split('/')[-1]
        data = requests.get(url)
        soup = BeautifulSoup(data.content, 'html.parser')

        new_articles = [{'news_headline': headline.find('span', attrs={"itemprop": "headline"}).string,
                         'news_article': article.find('div', attrs={"itemprop": "articleBody"}).string,
                         'news_category': news_category}
                        for headline, article in zip(soup.find_all('div', class_=['news-card-title news-right-box']),
                                                     soup.find_all('div', class_=['news-card-content news-right-box']))]
        new_data.extend(new_articles)

    df = pd.DataFrame(new_data)
    df = df[['news_headline', 'news_article', 'news_category']]
    return df


if __name__ == "__main__":
    news_df = build_dataset(seed_urls)
