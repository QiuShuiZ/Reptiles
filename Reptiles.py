import os
import requests
from pyquery import PyQuery as pq


class Model(object):
    """
    基类, 用来显示类的信息
    """

    def __repr__(self):
        name = self.__class__.__name__
        properties = ('{}=({})'.format(k, v) for k, v in self.__dict__.items())
        s = '\n<{} \n  {}>'.format(name, '\n  '.join(properties))
        return s


class Movie(Model):
    """
    存储信息
    """

    def __init__(self):
        self.cover_url = ''


def cached_url(url):
    """
        缓存, 避免重复下载网页浪费时间
        """
    folder = 'cached'
    filename = url.split('/')[-1] + '.html'
    'cached/0.html'
    path = os.path.join(folder, filename)
    if os.path.exists(path):
        with open(path, 'rb') as f:
            s = f.read()
            return s
    else:
        # 建立 cached 文件夹
        if not os.path.exists(folder):
            os.makedirs(folder)

        headers = {
            'user-agent': '''Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36
    Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8''',
        }
        # 发送网络请求, 把结果写入到文件夹中
        r = requests.get(url, headers)
        with open(path, 'wb') as f:
            f.write(r.content)
        return r.content


def movie_from_div(div):
    """
    从一个 div 里面获取到一个信息
    """
    e = pq(div)

    # 小作用域变量用单字符
    m = Movie()
    m.cover_url = e('img').attr('src')
    return m


def movies_from_url(url):
    """
    从 url 中下载网页并解析出页面
    """
    '''
    只会下载一次
    '''
    page = cached_url(url)
    e = pq(page)
    # print(page.decode())
    # 2.父节点
    items = e('img')
    # 调用 movie_from_div
    # list comprehension
    movies = [movie_from_div(i) for i in items]
    return movies


def download_image(url):
    # 每张图片的url
    folder = url.split("/")[-2]
    filename = url.split("/")[-1]
    path = os.path.join(folder, filename)

    if os.path.exists(path):
        return
    else:
        # 建立文件夹
        if not os.path.exists(folder):
            os.makedirs(folder)
        headers = {
            'user-agent': '''Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36
            Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8''',
        }
        # 发送网络请求, 把结果写入到文件夹中
        r = requests.get(url, headers)
        with open(path, 'wb') as f:
            f.write(r.content)


def main():
    for i in range(56, 68):
        url = 'https://www.conphotos.com/htm/photos0/{}.htm'.format(i)
        movies = movies_from_url(url)
        print('every_page', movies)
        [download_image(m.cover_url) for m in movies]
    # url = 'https://www.conphotos.com/htm/photos0/55.htm'
    # movies = movies_from_url(url)
    # print('every_page', movies)
    # [download_image(m.cover_url) for m in movies]


if __name__ == '__main__':
    main()
