#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   cookie_test.py
@Time    :   2019/03/12 17:07:45
'''

# here put the import lib
import requests
import browsercookie
from reverse_js import create_guid, create_cookie_key


# guid_value = create_guid()
# cookie_value = create_cookie_key()

# headers = {
#     "Host": "wenshu.court.gov.cn",
#     "Origin": "http://wenshu.court.gov.cn",
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
#     "X-Requested-With": "XMLHttpRequest",
#     "Referer": "http://wenshu.court.gov.cn/list/list/?sorttype=1&number=&guid=8c149c34-b14f-6a510140-68c2305c5925&conditions=searchWord+2+AJLX++%E6%A1%88%E4%BB%B6%E7%B1%BB%E5%9E%8B:%E6%B0%91%E4%BA%8B%E6%A1%88%E4%BB%B6"
# }
# data = {
#     "Param": "案件类型:民事案件,关键词:赡养",
#     "Index": "1",
#     "Page": "10",
#     "Order": "法院层级",
#     "Direction": "asc",
#     "vl5x": cookie_value,
#     "number": "&gui",
#     "guid": guid_value,
# }

# res = requests.post('http://wenshu.court.gov.cn/List/ListContent', headers=headers, data=data, cookies=cookiejar)
# res.encoding = 'utf-8'
# # print(res.text)
# # print(res.cookies)
# print(cookie_value)
# print(guid_value)
def get_vjkl5():
    vjx5_url = 'http://wenshu.court.gov.cn/list/list/?sorttype=1&number=&guid=69aa2cd1-7311-9ece2dc2-74a9f7100d76&conditions=searchWord+%E5%90%88%E5%90%8C+++%E5%85%B3%E9%94%AE%E8%AF%8D:%E5%90%88%E5%90%8C'
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
            # "Cookie": None,
        }
        res1 = requests.get(url=vjx5_url, headers=headers)
        # print(res1.json())
        print(type(res1.cookies))
        print(res1.headers)
    except requests.exceptions as e:
        print(e)


if __name__ == "__main__":
    get_vjkl5()
