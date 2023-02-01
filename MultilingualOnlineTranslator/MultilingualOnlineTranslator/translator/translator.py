import requests
from bs4 import BeautifulSoup
import argparse


class Translator:

    def __init__(self, from_lang, to_lang, word):
        self.headers = {'User-Agent': 'Mozilla/5.0'}
        self.url_core = "https://context.reverso.net/translation"
        self.__languages = {0: 'All', 1: 'Arabic', 2: 'German', 3: 'English', 4: 'Spanish', 5: 'French', 6: 'Hebrew',
                            7: 'Japanese', 8: 'Dutch', 9: 'Polish', 10: 'Portuguese',
                            11: 'Romanian', 12: 'Russian', 13: 'Turkish'}

        self.from_lang = from_lang
        self.to_lang = to_lang
        self.word = word

    def main(self):
        if self.from_lang.title() not in self.__languages.values():
            print(f"Sorry, the program doesn't support {self.from_lang}")
            return
        elif self.to_lang.title() not in self.__languages.values():
            print(f"Sorry, the program doesn't support {self.to_lang}")
            return

        if self.to_lang != "all":
            soup = self.get_web_content(self.to_lang)

            if soup:
                self.get_translations(soup)
                self.get_examples(soup)
            else:
                print('Please try again')
        else:
            for lang in self.__languages.values():
                if lang == 'All':
                    continue
                soup = self.get_web_content(lang)
                if soup:
                    self.get_translations(soup, lang, multi=True)
                    self.get_examples(soup, lang, multi=True)
        with open(f'{self.word}.txt', 'r', encoding='utf-8') as f:
            for el in f.readlines():
                print(el, end='')

    def get_web_content(self, direction_lang):
        url = f"{self.url_core}/{self.from_lang.lower()}-{direction_lang.lower()}/{self.word}"
        page = requests.get(url, headers=self.headers)
        conn_status = page.status_code

        if conn_status == 200:
            return BeautifulSoup(page.content, 'html.parser')
        elif conn_status == 404:
            print("Something wrong with your internet connection")
            return False
        else:
            print('Something wrong with your internet connection')
            return False

    def get_translations(self, soup, language=None, multi=False):
        paragraphs = soup.find_all('span', {'class': 'display-term'})
        translations = []

        for i in paragraphs:
            translations.append(i.text)

        if len(translations) == 0:
            print(f"Sorry, unable to find {self.word}")
            return

        elif multi:
            self.add_to_file(f'{language} Translations:')
            self.add_to_file(translations[0] + '\n')
        else:
            self.add_to_file(f'{self.to_lang} Translations:')
            for el in translations:
                self.add_to_file(el)

    def get_examples(self, soup, language=None, multi=False):
        lines = soup.find_all('div', {'class': ['src ltr', 'trg ltr']})

        if not multi:
            self.add_to_file("\n" + f'{self.to_lang} Examples:')

            for i, line in enumerate(lines):
                if i % 2 == 0 and i != 0:
                    # print()
                    self.add_to_file('\n')
                tmp_example = (" ".join(line.text.split()))
                if len(tmp_example) == 0:
                    continue
                else:
                    # print(tmp_example)
                    self.add_to_file(tmp_example)

        elif multi:
            if language == self.from_lang:
                return
            self.add_to_file(f'{language} Example:')
            for i, line in enumerate(lines):
                if i < 2:
                    tmp_example = (" ".join(line.text.split()))
                    self.add_to_file(tmp_example)
            self.add_to_file('\n')
        else:
            print('Something went wrong with get_examples')

    def add_to_file(self, content):
        with open(f'{self.word}.txt', 'a+', encoding='utf-8') as f:
            f.write(content + '\n')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="This program translates words using context.reverso.net"
    )
    parser.add_argument("from_lang")
    parser.add_argument("to_lang")
    parser.add_argument("word")
    args = parser.parse_args()

    translator = Translator(args.from_lang, args.to_lang, args.word)
    translator.main()
