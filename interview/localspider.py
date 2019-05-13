#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   localspider.py
@Time    :   2019/05/11 20:13:14
'''

import asyncio
import re
import aiohttp
import os

base_url = 'http://127.0.0.1:8080/'
dir_path = os.path.dirname(__file__) + '/localspider/'
url_set = set() # fetch set
file_set  = set() # all download files url (option)
filter_set = set() # filter set

async def fetch(url):
    """
    请求方法
    
    Arguments:
        url {str} -- 目标页面url
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                res_dict = {}
                res_dict['page_data'] = await response.read() # binary data 
                res_dict['request_url'] = url
                return res_dict
            else:
                print('Bad request :%s'%url)

async def parse(url, data):
    """
    解析方法：
        当确定请求的url是一个单独文件时，会触发储存方法。
        此处也可将储存方法移除，启用file_set文件过滤器。最后在储存函数中并发请求file_set中的url

    Arguments:
        url {str} -- 目标页面url
        data {bin} -- 从页面请求到的数据
    """
    alink_list = re.findall('<a href=".*?">(.*?)</a>', str(data), re.S)
    for link in alink_list:
        if link.endswith('/') and '../' not in link and link not in filter_set: 
            url_set.add(url + link) # collecting url for deep crawl
            filter_set.add(url + link) # add to filter
            print("-- adding url:%s"%(url + link))
        elif link not in file_set and '../' not in link and link not in file_set:
            file_url = url + link
            file_set.add(file_url) # add to file_set (option)
            await save_data(file_url)
            print('adding file_url: %s'%file_url)

async def deep_crawl():
    """
    深度爬取方法：
        由fetch方法和parse方法构成

    """
    has_more = 1
    while has_more:
        multi_data = await asyncio.gather(*[fetch(url) for url in url_set]) # multi_page type(list)
        url_set.clear() # filter_set can track all the url we get
        for data in multi_data:
            await parse(data['request_url'], data['page_data']) # get single page data, new url will add to url_set in this step
        if len(url_set) == 0:
            has_more = 0

async def save_data(url):
    """
    储存方法：
        此方法中包含了文件存储、文件名和路径的提取以及文件夹的动态生成
        其中从对应的url中提取路径和文件名可以单独写为mod_url(当提取或生成难度增加时)

    Arguments:
        url {str} -- 目标文件url
    """
    if 'ecstatic' not in url:
        raw_data = await fetch(url)
        url = url.replace('http://127.0.0.1:8080', '') # extract file_path & file_name
        file_info = os.path.split(url)
        file_path = file_info[0]
        file_name = file_info[1]
        file_data = raw_data['page_data']
        if not os.path.exists(dir_path + file_path): # dynamic create diractory 
            os.makedirs(dir_path + file_path)
        try:
            with open(r'{dir_path}/{file_path}/{file_name}'.format(file_path=file_path, dir_path=dir_path, file_name=file_name), 'wb') as f:
                f.write(file_data)
                f.close()
        except Exception as e:
            print('save_data error: %s'%e)

async def mod_url(url):
    pass

async def mk_dir(url):
    pass


async def main():
    """
    主函数

    """
    raw_content = await fetch(url=base_url) # get index page
    await parse(raw_content['request_url'], raw_content['page_data'])
    await deep_crawl()
    


if __name__ == '__main__':
    print("--start--")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    print("--end--")







