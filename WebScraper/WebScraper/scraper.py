import string

import requests
from bs4 import BeautifulSoup
import os


class GetServerResponseMixin:
    def __init__(self):
        self.soup = None

    def get_server_response(self, url):
        response = requests.get(url, headers={'Accept-Language': 'en-US,en;q=0.5'}, timeout=None)
        if response.status_code == 200:
            self.soup = BeautifulSoup(response.content, 'html.parser')
        else:
            print(response.status_code)
            exit('Connection interruption')


class ArticlesAtMainPage(GetServerResponseMixin):
    def __init__(self, pages, article_type):
        self.pages = pages
        self.page = None
        self.article_type = article_type
        self.articles = None
        self.base_url = f'https://www.nature.com/nature/articles?sort=PubDate&year=2020&page='
        self.dir_name = None
        self.path = None
        self.url = None
        super().__init__()

    def get_articles_list(self):
        self.articles = self.soup.find_all('article')

    def parse_articles(self):
        self.get_server_response(self.url)
        self.get_articles_list()

        for nature_article in self.articles:
            if nature_article.find('span',
                                   {
                                       'class': 'c-meta__type'}).text == self.article_type:  # filter tagged articles
                article = Article(nature_article)
                article.parse_content()
                article.save_to_file(self.dir_name)


    def main(self):
        for page in range(1, self.pages + 1):
            self.page = str(page)
            self.url = self.base_url + self.page
            self.dir_name = f'Page_{page}'
            if not os.path.isdir(self.dir_name):
                os.mkdir(self.dir_name)
            self.parse_articles()


class Article(GetServerResponseMixin):
    def __init__(self, nature_article):
        self.path = None
        self.nature_article = nature_article
        self.title = ''
        self.file_name = ''
        self.url = None
        self.content = None
        super().__init__()

    def parse_title_and_link(self):
        title_and_link = self.nature_article.find('a', {'data-track-action': 'view article'})
        self.title = title_and_link.text
        self.file_name = '_'.join([x.strip(string.punctuation) for x in self.title.split()])
        self.url = f"https://www.nature.com{title_and_link.get('href')}"

    def parse_body(self):
        body = self.soup.find('div', {'class': 'c-article-body'})
        self.content = body.text

    def parse_content(self):
        self.parse_title_and_link()
        self.get_server_response(self.url)
        self.parse_body()

    def save_to_file(self, dir_name):
        self.path = dir_name + '/' + self.file_name

        try:
            with open(f'{self.path}.txt', 'wb') as f:
                if self.content.encode('UTF-8'):
                    f.write(self.content.encode('UTF-8'))
                    print('Content saved.')
                else:
                    print('empty file')
                    return
        except Exception as e:
            print(f'Error: {e}')


if __name__ == "__main__":
    input_page = int(input())
    input_article_type = input()
    nature = ArticlesAtMainPage(input_page, input_article_type)
    nature.main()
