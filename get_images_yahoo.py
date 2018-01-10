
# coding: utf-8

# In[ ]:


# coding: utf-8

import os #OSモジュール（OSとの対話モジュール）のインポート
import sys #sysモジュール（インタプリタの動作関連モジュール）のインポート
import traceback #スタックトレースを抽出し、書式を整える
from mimetypes import guess_extension #mime型に基いて拡張子を推定する関数
from time import time, sleep #時間に関する関数を提供するモジュール
from urllib.request import urlopen, Request #URLを読み込むためのモジュール
from urllib.parse import quote #URLをパースするためのモジュール
from bs4 import BeautifulSoup #ビューティフルスープ

MY_EMAIL_ADDR = 'takano@ryujifujimura.jp'

class Fetcher:
    def __init__(self, ua=''):  #コンストラクタ
        self.ua = ua

    def fetch(self, url):   #fetch()メソッド
        req = Request(url, headers={'User-Agent': self.ua})
        try:
            with urlopen(req, timeout=3) as p:
                b_content = p.read()
                mime = p.getheader('Content-Type')
        except:
            sys.stderr.write('Error in fetching {}\n'.format(url))
            sys.stderr.write(traceback.format_exc())
            return None, None
        return b_content, mime

fetcher = Fetcher(MY_EMAIL_ADDR)

def fetch_and_save_img(word):   #データを保存するメソッド
    data_dir = 'data/'
    if not os.path.exists(data_dir): #data_dirがなかったら
        os.makedirs(data_dir)       #data_dirを作成(osモジュールによる)

    for i, img_url in enumerate(img_url_list(word)):
        sleep(0.1)
        img, mime = fetcher.fetch(img_url)
        if not mime or not img:
            continue
        ext = guess_extension(mime.split(';')[0])
        if ext in ('.jpe', '.jpeg'):
            ext = '.jpg'
        if not ext:
            continue
        result_file = os.path.join(data_dir, str(i) + ext)
        with open(result_file, mode='wb') as f:
            f.write(img)
        print('fetched', img_url)


def img_url_list(word):
    """    using yahoo (this script can't use at google    """
    url = 'http://image.search.yahoo.co.jp/search?n=60&p={}&search.x=1'.format(quote(word))
    byte_content, _ = fetcher.fetch(url)
    structured_page = BeautifulSoup(byte_content.decode('UTF-8'), 'html.parser')
    img_link_elems = structured_page.find_all('a', attrs={'target': 'imagewin'})
    img_urls = [e.get('href') for e in img_link_elems if e.get('href').startswith('http')]
    img_urls = list(set(img_urls))
    return img_urls

if __name__ == '__main__':
    word = sys.argv[1]
    fetch_and_save_img(word)
