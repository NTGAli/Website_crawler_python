import requests
from bs4 import BeautifulSoup
from newspaper import Article
from tqdm import tqdm
import pandas as pd

if __name__ == '__main__':
    # start with this page
    page = 1
    scraped_date = []
    while True:
        page += 1
        # url of main page
        main_page_url = f"https://digiato.com/page/{page}"

        html = requests.get(main_page_url).text
        soup = BeautifulSoup(html, 'lxml')

        links = soup.find_all('h3')

        if len(links) == 0:
            break

        for link in tqdm(links):
            page_url = link.a['href']
            try:
                 article = Article(page_url)
                 article.download()
                 article.parse()
                 scraped_date.append({'url': page_url, 'text': article.text, 'title': article.title})
            except:
                print(f"Faild Page: {page_url}")

        print(f"len: {len(scraped_date)}, page: {page}")
        df = pd.DataFrame(scraped_date)
        df.to_csv(f'digiato2.csv')

        # digiato.csv is test there are near 5000 record
        # Note: Depending on the website you are considering, you may need to change some of the code
