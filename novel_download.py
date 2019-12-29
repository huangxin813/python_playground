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
        self.urls = []

    def init_links(self):
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
                self.chapters.append(a.text)
                self.urls.append(base_url + a.get('href'))

    def download_content(self, url):
        r = requests.get(url);
        r.encoding = 'gbk'
        soup = BeautifulSoup(r.text, 'html.parser')
        for script in soup(['script']):
            script.extract()
        content = soup.find_all('div', class_ = 'showtxt')
        return content[0].text.replace('\xa0'*8, '').replace('\r\n', '\n')

    def write(self, chapter, text):
        with open('./novel/' + chapter + '.txt', 'w', encoding='utf-8') as f:
            f.write(chapter + '\n')
            f.writelines(text + '\n'*3)
        f.close()

if __name__ == '__main__':
    d = NovelDownloader()
    d.init_links()
    for chapter, url in zip(d.chapters[0: 10], d.urls[0: 10]):
        content = d.download_content(url)
        d.write(chapter, content)
