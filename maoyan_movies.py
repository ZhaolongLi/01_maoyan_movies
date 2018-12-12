# coding:utf-8

import requests
import re
import json
import time

from requests.exceptions import RequestException


def get_one_page(url):
    """
    抓取首页
    :param url:
    :return:
    """
    try:
        headers = {
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) '
                         'AppleWebKit/535.11 (KHTML, like Gecko) Chrome/' 
                         '17.0.963.56 Safari/535.11'
        }
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

def parse_one_page(html):
    """
    提取第一页中的相关内容
    :param html:
    :return:
    """
    pattern = re.compile( # 使用正则表达式提取
        '<dd>.*?board-index.*?>(.*?)</i>.*?data-src="(.*?)".*?name.*?a.*?>(.*?)'
        '</a>.*?star.*?>(.*?)</p>.*?releasetime.*?>(.*?)</p>.*?integer.*?>(.*?)'
        '</i>.*?fraction.*?>(.*?)</i>.*?</dd>',re.S
    )
    items = re.findall(pattern,html)
    # print(items)
    for item in items:
        yield {
            'index':item[0],
            'image':item[1],
            'title':item[2].strip(),
            'actor':item[3].strip()[3:] if len(item[3]) > 3 else '',
            'time':item[4].strip()[5:] if len(item[4]) > 5 else '',
            'score':item[5].strip() + item[6].strip()
         }

def write_to_file(content):
    """
    将提取的内容写到文件中
    :param content:
    :return:
    """
    with open('result.txt','a',encoding='utf-8') as f:
        # print(type(json.dumps(content)))
        f.write(json.dumps(content,ensure_ascii=False)+'\n') # 确保中文能够写入


def main(offset):
    url = 'http://maoyan.com/board/4?offset=' + str(offset)
    html = get_one_page(url)
    # print(html)
    for item in parse_one_page(html):
        write_to_file(item)


if __name__ == '__main__':
    for i in range(10):
        main(offset=i*10)
        time.sleep(1)

