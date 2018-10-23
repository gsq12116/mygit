import json

import requests
import re


def get_page(url):
    headers = {
        "User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.content.decode('utf-8')  # 字节流,对应response.text字符串
    return None


def parse_page(html):
    movie_page = []
    pattern0 = re.compile('movieId.*?>.*?<img.*?<img.*?alt="(.*?)" class.*?', re.S)
    results0 = re.findall(pattern0, html)
    pattern1 = re.compile('<p class="star">(.*?)</p>', re.S)
    results1 = re.findall(pattern1, html)
    pattern2 = re.compile('<p class="releasetime">(.*?)</p>', re.S)
    results2 = re.findall(pattern2, html)
    pattern3 = re.compile('movieId.*?<img.*?<img.*?src="(.*?)".*?</a>', re.S)
    results3 = re.findall(pattern3, html)
    for i in range(len(results1)):
        movie = {}
        movie['title'] = results0[i].strip()
        movie['staring'] = results1[i].strip()
        movie['release_time'] = results2[i]
        movie['img'] = results3[i].split('@')[0].split('/')[-1]
        movie_page.append(movie)
    return movie_page


def write_img(url):
    response = requests.get(url)
    first = url.split('@')[0]
    seconed = first.split('/')[-1]
    with open('./img/%s' % seconed, 'wb') as f:
        f.write(response.content)


def main():
    movies = {}
    for i in range(10):
        url = 'http://maoyan.com/board/4?offset=%d' % (i*10)
        html = get_page(url)
        results = parse_page(html)
        page_name = 'page%d' % (i+1)
        movies[page_name] = results
    with open('./movies/movies_info.json', 'w', encoding='utf-8') as f:
        a = json.dumps(movies, ensure_ascii=False)
        f.write(a)
        # for result in results:
        #     图片存储
        #     write_img(result)
        # print(html)
        # print(result)


if __name__ == '__main__':
    main()