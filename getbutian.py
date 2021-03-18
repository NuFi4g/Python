#!/usr/bin/python3
# coding: utf-8
'''
@Time    :   2020-03-05 12:19:23
@Author  :   NuFi4g
@Desc    :   爬取补天公益SRC厂家地址脚本
'''

import json
import requests
import time
from bs4 import BeautifulSoup
"""
爬取补天公益SRC厂家id
"""


def get_id():
    headers = {
        'Host': 'www.butian.net',
        'User-Agent':
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:73.0) Gecko/20100101 Firefox/73.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language':
        'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'https://www.butian.net',
        'Connection': 'keep-alive',
        'Referer': 'https://www.butian.net/Reward/plan/Message/send',
        'Cookie': 'PHPSESSID=XXXXXXX'  # 未登陆时的cookie
    }

    for i in range(1, 2):  # 1~178
        data = {'p': i, 'token': ''}
        time.sleep(3)
        res = requests.post('https://www.butian.net/Reward/pub/Message/send',
                            data=data,
                            headers=headers,
                            timeout=(4, 20))
        allResult = {}
        allResult = json.loads(res.text)
        currentPage = str(allResult['data']['current'])
        currentNum = str(len(allResult['data']['list']))
        print('正在获取第' + currentPage + '页厂商数据')
        print('本页共有' + currentNum + '条厂商')
        for num in range(int(currentNum)):
            company_id = allResult['data']['list'][int(num)]['company_id']
            base = 'https://www.butian.net/Loo/submit?cid='
            with open('butian_reptile/company_id.txt', 'a') as f:
                f.write(base + company_id + '\n')
    print('[*] The id is right!')


"""
获取id对应的厂家网站url
"""


def get_url():
    headers = {
        'Host': 'www.butian.net',
        'User-Agent':
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:73.0) Gecko/20100101 Firefox/73.0',
        'Accept':
        'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language':
        'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Referer': 'https://www.butian.net/Reward/plan',
        'Cookie': 'PHPSESSID=XXXXXX',  # 登陆后的cookie
        'Upgrade-Insecure-Requests': '1'
    }
    with open('butian_reptile/company_id.txt', 'r') as f:
        for target in f.readlines():
            target = target.strip()
            getUrl = requests.get(target, headers=headers, timeout=(4, 20))
            result = getUrl.text
            info = BeautifulSoup(result, 'html.parser')
            url = info.find(name='input', attrs={"name": "host"})
            name = info.find(name='input', attrs={"name": "company_name"})
            realUrl = url.attrs['value']
            company_info = target + '\t' + name.attrs[
                'value'] + '\t' + url.attrs['value']
            with open('butian_reptile/company_url.txt', 'a') as t:
                t.write(realUrl + '\n')
            with open('butian_reptile/company_info.txt', 'a') as i:
                i.write(company_info + '\n')
            time.sleep(3)
    print('[*] The target is right!')


if __name__ == "__main__":
    data = {'s': '1', 'p': '1', 'token': ''}
    res = requests.post('https://www.butian.net/Reward/pub/Message/send',
                        data=data)
    allResult = {}
    allResult = json.loads(res.text)
    allPages = str(allResult['data']['count'])
    print('共' + allPages + '页')

    get_id()
    get_url()
