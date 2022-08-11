import requests
import bs4
from pprint import pprint
import re


class HabrArticleSorter:
    def __init__(self, keywords):
        self.keywords = keywords
        self.url = 'https://habr.com'
        self.headers = {'Cookie': '_ym_uid=1612867515208540576; _ga=GA1.2.107181986.1634321921; fl=ru; hl=ru; __gads=ID=860de5367279e173:T=1634417832:S=ALNI_MYJ3WVnwOp62nHtEr6fICBogRYJxg; feature_streaming_comments=tr',
                        'Accept-Language': 'ru,en;q=0.9,hr;q=0.8',
                        'Sec-Fetch-Dest': 'document',
                        'Sec-Fetch-Mode': 'navigate',
                        'Sec-Fetch-Site': 'same-origin',
                        'Sec-Fetch-User': '?1',
                        'Cache-Control': 'max-age=0',
                        'sec-ch-ua-mobile': '?0',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.148 YaBrowser/22.7.2.899 Yowser/2.5 Safari/537.36'}

    def get_articles(self):
        response = requests.get(url=self.url+'/ru/all/', headers=self.headers)
        text = response.text
        soup = bs4.BeautifulSoup(text, features='html.parser')
        articles = soup.find_all(class_="tm-article-snippet")
        return articles

    def articles_sorter(self):
        sorted_articles = []
        article_dict = {}
        articles = self.get_articles()

        for article in articles:
            title = article.find('h2').find('a')
            href = title.attrs['href']
            date_time = article.find('time').attrs['title']
            hubs = article.find_all('span', class_='tm-article-snippet__hubs-item')
            hubs = [hub.find('a').text.strip() for hub in hubs]
            hubs = ' '.join(hubs)
            contents = article.find('div', class_="article-formatted-body article-formatted-body article-formatted-body_version-2")
            if contents:
                contents = contents.find_all('p')
                contents = [content.text.strip() for content in contents]
                article_dict['content'] = ' '.join(contents)
            contents = article.find_all('div', class_="article-formatted-body article-formatted-body article-formatted-body_version-1")
            if contents:
                contents = [content.text.strip() for content in contents]
                article_dict['content'] = ' '.join(contents)
            article_dict['title'] = title.text
            article_dict['href'] = self.url + href
            article_dict['date'] = date_time
            article_dict['hubs'] = hubs
            sorted_articles.append(article_dict)
            article_dict = {}

        return sorted_articles

    def filter_articles(self):
        articles = self.articles_sorter()
        print(f'Статьи отфильтрованы по ключевым словам: {self.keywords}.\n')
        for element in articles:
            for word in self.keywords:
                if re.findall(word, element['title'], flags=re.IGNORECASE):
                    print(f'<{element["date"]}> - <{element["title"]}> - <{element["href"]}')
                elif re.findall(word, element['hubs'], flags=re.IGNORECASE):
                    print(f'<{element["date"]}> - <{element["title"]}> - <{element["href"]}')
                elif re.findall(word, element['content'], flags=re.IGNORECASE):
                    print(f'<{element["date"]}> - <{element["title"]}> - <{element["href"]}')
