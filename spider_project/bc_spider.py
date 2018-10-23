import json
import re

import requests
from bs4 import BeautifulSoup

from conn_object.conn_db import Conn


def get_one_page(url):
    # url = "http://bbs.orzice.com/forum-138-6.html"
    headers = {
        "User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        text = response.content.decode('utf-8')
        return text
    return None


def parse_soup(html, flag=True):
    page_info = []
    soup = BeautifulSoup(html, 'lxml')
    titles = soup.select('#threadlisttableid tbody tr th.new a.xst')
    authors = soup.select('#threadlisttableid tbody tr td.by')
    titles_info = [title.string for title in titles]
    if flag:
        authors_info = [author.a.string for author in authors[2::2]]
        times_info = [author.em.span.string for author in authors[2::2]]
    else:
        authors_info = [author.a.string for author in authors[4::2]]
        times_info = [author.em.span.string for author in authors[4::2]]
    for i in range(len(titles_info)):
        info = {}
        info['title'] = titles_info[i]
        info['author'] = authors_info[i]
        info['create_time'] = times_info[i]
        page_info.append(info)
    return page_info

def main():
    conn = Conn('localhost', 3306, 'root', '', 'spider')
    for i in range(130):
        flag = True
        if i == 0:
            flag = False
        url = "http://bbs.orzice.com/forum-138-%d.html" % (i+1)
        html = get_one_page(url)
        page_name = 'page%d' % (i+1)
        page_info = parse_soup(html, flag)
        print(page_name+' complete')
        for obj in page_info:
            ability_title = re.sub('\'', "''", obj['title'])
            sql = "insert into forum(title, author, create_time) values('"+ability_title+"', '"+obj['author']+"', '"+obj['create_time']+"')"
            conn.exec_sql(sql)
    conn.conn_close()
    # with open('xxx.json', 'w', encoding='utf-8') as f:
    #     s = json.dumps(spider_dict, ensure_ascii=False)
    #     f.write(s)


if __name__ == '__main__':
    # main()
    # with open('xxx.json', 'r', encoding='utf-8') as f:
    #     s = json.load(f)
    #     print(len(s))
    one = Conn('localhost', 3306, 'root', '', 'spider')
    result = one.select('select * from forum')
    one.conn_close()
    for i in result:
        print(i)
