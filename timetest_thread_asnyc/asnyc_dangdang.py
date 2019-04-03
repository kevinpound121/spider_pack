import asyncio
import aiohttp
import pandas as pd
from pyquery import PyQuery as pq
import time


async def request(url):
    session = aiohttp.ClientSession()
    res = await session.get(url)
    result = await res.text(encoding='gb18030') # 兼容gb2312
    doc = pq(result)
    # 生成pq对象，可迭代
    items = doc('.bang_list').children().items()
    session.close()
    return items


async def parse_content(items):
    for i in items:
        rank = i('.list_num').text().strip('.')
        name = i('.name a').text()
        commments = i('.star a').text().strip('条评论')
        # eq指定第几个元素
        author = i('.publisher_info a').eq(0).text()
        publisher = i('.publisher_info a').eq(2).text() if len(i('.publisher_info a').eq(2).text()) >= 2 else ''
        data_list.append([rank, name, commments, author, publisher])


async def main(url):
    content = await request(url)
    await parse_content(content)

data_list = []
urls = ['http://bang.dangdang.com/books/bestsellers/1-{}'.format(i) for i in range(1,51)]

# 时间统计
t1 = time.time()
# 加载事件循环
loop = asyncio.get_event_loop()
tasks = [asyncio.ensure_future(main(url)) for url in urls]
# tasks = asyncio.gather(*tasks)
loop.run_until_complete(asyncio.wait(tasks))

df = pd.DataFrame(data_list, columns=['rank', 'name', 'comments', 'author', 'publisher'])
df.to_csv('./dangdang-top.csv', index=False, encoding='utf-8-sig')

t2 = time.time()

print('使用异步协程的时间是：%s'%(t2-t1))
