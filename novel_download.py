import requests
from bs4 import BeautifulSoup
import re

"""
练习
"""
class NovelDownloader(object):

    def __init__(self):
        super().__init__()
        self.chapters = []

    def init_chapters(self):
        base_url = 'https://www.biqukan.com/'
        table_url = 'https://www.biqukan.com/1_1094/'
        r = requests.get(table_url)
        r.encoding = 'gbk'
        soup = BeautifulSoup(r.text, 'html.parser')
        divs = soup.find_all('div', class_ = 'listmain')
        a_soup = BeautifulSoup(str(divs[0]), 'html.parser')
        a_array = a_soup.find_all('a')
        for a in a_array[13: 100]:
            if (re.match(r'第+章*', a.text)):
                chapter = Chapter(a.text, base_url + a.get('href'))
                self.chapters.append(chapter)

    def get_chapter_content(self, chapter):
        r = requests.get(chapter.get_url());
        r.encoding = 'gbk'
        soup = BeautifulSoup(r.text, 'html.parser')
        for script in soup(['script']):
            script.extract()
        content = soup.find_all('div', class_ = 'showtxt')
        text = content[0].text.replace('\xa0'*8, '').replace('\r\n', '\n')
        chapter.set_content(text)
        return text


    def write(self, chapter):
        with open('./novel/' + chapter.get_name() + '.txt', 'w', encoding='utf-8') as f:
            f.write(chapter.get_name() + '\n')
            f.writelines(chapter.get_content() + '\n'*3)

"""
章节
"""
class Chapter:
    def __init__(self, name, url):
         self.name = name
         self.url = url
         self.content = None

    def get_name(self):
        return self.name

    def get_url(self):
        return self.url

    def get_content(self):
        return self.content

    def set_content(self, text):
        self.content = text


if __name__ == '__main__':
    d = NovelDownloader()
    d.init_chapters()
    for chapter in d.chapters[0: 10]:
        d.get_chapter_content(chapter)
        d.write(chapter)
