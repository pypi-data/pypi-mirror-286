#!/usr/bin/env python
# coding: utf-8

import re
import requests
from bs4 import BeautifulSoup

def parse_url(url):
    response = requests.get(url)
    if (response.status_code != 200):
        print('error access url', response.status_code)
        return
    a = re.findall('(href=".*?download=true)', response.text)
    all = []
    for i in a:
        _url = i.replace('?download=true','').replace('href="', 'https://hf-mirror.com')
        dst = ' out='+_url.split('main/')[-1]
        all.append([_url, dst])
    return all

def parse_dir(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    dirs=[]
    uls = soup.find_all('ul')
    for ul in uls[0:]:
        lis = ul.find_all('li')  # 提取每个ul下的li元素
        for li in lis:
            a = re.findall('href="([^\"]*)"', str(li))
            if len(a) == 0:
                continue
            a = a[0]
            if 'tree' in a:
                dirs.append(a)
    return dirs

def parse_main(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    ds = parse_dir(url)

    _all = []
    for d in ds:
        t = parse_url('https://hf-mirror.com'+d)
        _all.extend(t)
    return _all


url = 'https://hf-mirror.com/RunDiffusion/Juggernaut-XL-v9/tree/main'

# print('-=-=-==-=')
# print(parse_main(url))


