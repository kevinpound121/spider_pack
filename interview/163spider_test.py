#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   163spider_test.py
@Time    :   2019/04/29 10:40:42
'''

import asyncio
import os
import re
import aiohttp
from aiohttp import TCPConnector


url = 'https://www.163.com/'
headers = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate, br',
    'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8',
    'Cache-Control':'max-age=0',
    'Connection':'keep-alive',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
}
file_path = os.path.dirname(__file__)
url_filter = set()
target_url = set() #  save_page url

async def get_page(url, headers=headers):
    """
    请求方法：
    请求目标页面并提取页面内容，编码方式
    
    Arguments:
        url {str} -- 需查询的页面url
    
    Keyword Arguments:
        headers {dict} -- 请求头部 (已设置为默认，可更改) (default: {headers})
    """
    try:
        async with aiohttp.ClientSession(connector=TCPConnector(verify_ssl=False)) as session:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    print("fetch url: %s -- OK"%url)
                    res_dict = {}
                    res_dict['response_html'] = await response.text() # page data (str)
                    res_dict['encode_type'] = response.get_encoding() # for save_page() encoding type
                    res_dict['request_url'] = url # for save_page() url_filename
                    # res_dict['response_raw_data'] = await response.read() # binary data (option)
                    return  res_dict
    except Exception as e:
        print("get page failed as:%s"%e)

async def parse_page(url, html): 
    """
    解析方法：
    提取页面链接
    
    Arguments:
        url {str} -- 用于判断是否为首页
        html {str} -- 用于提取链接的页面数据
    """
    try:
        if url == 'https://www.163.com/':
            print('---index page started---')
            nav_link = re.findall('<li class="liw\d">(.*?)</li>', html, re.S)
            alink = re.findall('<a.*?href="(.*?)".*?>', str(nav_link), re.S)
            link_list = alink[0:20:2]
            print(link_list)
            return link_list
        else:
            print('parse page url: %s'%url)
            alink = re.findall('<a.*?href="(h.*?)".*?>', html, re.S)
            return alink
    except Exception as e:
        print('parse page failed as %s'%e)

async def extract_links(url_list, limit=5):
    """
    链接提取+去重方法：
    本方法以get_page以及parse_page为基础，同时使用了url_filter以及target_url两个集合
    在保证了目标url的唯一性同时，也加强了函数的复用性。
    同时引入并发机制，提高了请求效率。
    
    Arguments:
        url_list {list} -- 需要提取链接页面的url列表
    
    Keyword Arguments:
        limit {int} -- 本次提取每页获取链接的数量 (default: {5})
    """
    multi_page = await asyncio.gather(*[get_page(url) for url in url_list]) # 10 response in multi_page list
    # print('---multi_page data list length:%s---'%len(multi_page))
    has_more = 1 
    while has_more:
        single_page = multi_page.pop()
        url_filter.add(single_page['request_url']) # add to the filter
        alink = await parse_page(single_page['request_url'], single_page['response_html']) 
        link_num = 0 # 
        for link in alink:
            if link not in url_filter and link_num < limit and link not in target_url:
                target_url.add(link)
                link_num += 1
        if len(multi_page) == 0:
            has_more = 0
    # return list(target_url) # unnecessary

async def save_page(url, html, encode_type):
    """
    页面存储方法：
    将获得的目标页面数据保存为html文件
    
    Arguments:
        url {str} -- 需要存储页面的url，用于构造文件名
        html {str} -- 需要存储页面的页面数据
        encode_type {str} -- 对应页面的编码方法，当utf-8编码方式失效时，用此备用选项进行编码
    """
    if len(html) > 0: # connection issue 
        # fix the filename illegal problem
        url = url.replace('http:', 'http;')
        url = url.replace('https:', 'https;')
        url = url.replace('\/', '^')
        url = url.replace('/', '_')
        url = url.replace('?', '%')
        url = url.replace('"', '$')
        url = url.replace('<', '#')
        url = url.replace('>', '!')
        url = url.replace('|', '~')
        url = url.replace('.html', '')
        try:
            with open(r'{file_path}/page2/{url}.html'.format(file_path=file_path, url=url), 'w', encoding='utf-8') as f:
                f.write(html)
                f.close()
        except Exception as e: 
            print("page save failed as:%s"%e)
            with open(r'{file_path}/page2/{url}.html'.format(file_path=file_path, url=url), 'w', encoding=encode_type) as f:
                f.write(html)
                f.close()
    else:
        print("---Bad url:%s, no content in this page---"%url)

async def async_main(url, headers): 
    """
    主逻辑方法：
    为保持save_page的独立程度，暂未将get_page引入该方法。
    如爬取深度加大可在主函数处增加depth参数。

    Arguments:
        url {str} -- 默认为163首页url，全局设定
        headers {dict} -- 默认请求头部，全局设定
    """
    index_page = await get_page(url)
    index_link = await parse_page(index_page['request_url'], index_page['response_html'])
    await extract_links(index_link)
    target_pages = await asyncio.gather(*[get_page(url) for url in target_url])
    for page in target_pages:
        try:
            await save_page(page['request_url'], page['response_html'], page['encode_type'])
        except Exception as e:
            print(e)
    # # 深度爬取代码
    # for i in depth:
    #     if depth < 0:
    #         target_pages = await asyncio.gather(*[get_page(url) for url in target_urls])
    #         for page in target_pages:
    #             try:
    #                 await save_page(page['request_url'], page['response_html'], page['encode_type'])
    #             except Exception as e:
    #                 print(e)
    #     else:
    #         await extract_links(target_url)
    #         depth -= 1
        
            



if __name__ == "__main__":
    print('Get started')
    loop = asyncio.get_event_loop()
    loop.run_until_complete(async_main(url, headers))
    print('This is the end')
