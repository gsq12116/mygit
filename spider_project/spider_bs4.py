"""new python"""
import requests
from bs4 import BeautifulSoup


def get_one_page():
    url = "http://300.jumpw.com/index.html?cid=0"
    headers = {
        "User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        text = response.content.decode('utf-8')
        return text
    return None


def parse_soup(html):
    soup = BeautifulSoup(html, 'lxml')
    # print(soup.prettify())
    print(soup.title.string)
    print(list(soup.meta.next_siblings)[1].attrs['content'])


def main():
    html = get_one_page()
    parse_soup(html)


if __name__ == '__main__':
    main()
