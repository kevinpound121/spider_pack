import aiohttp
import asyncio
from lxml import etree
import time
from pymongo import MongoClient

client = MongoClient()
db = client.lianjia
collection = db.lianjia2
end_page = 101
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"}



async def get_html(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                html = await response.text()
                doc = etree.HTML(html)
                div_list = doc.xpath('//li[@class="clear LOGCLICKDATA"]')
                for div in div_list:
                    item = {
                        "title": div.xpath('.//div[@class="title"]/a/text()')[0],
                        "href": div.xpath('.//div[@class="title"]/a/@href')[0],
                        "totalPrice": div.xpath('.//div[@class="totalPrice"]/span/text()')[0],
                        "houseInfo": div.xpath('.//div[@class="houseInfo"]/text()')[0],
                    }
                    await save_to_mongo(item)
            return None

async def save_to_mongo(item):
    if item:
        collection.insert(item)
        # print('保存到MongoDB成功')


async def request():
    url_list = ["https://gz.lianjia.com/ershoufang/pg{}/".format(i) for i in range(1, end_page)]
    async with  Pool() as pool:

        await pool.map(get_html, url_list)

def main():
    start_time = time.time()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(request())
    end_time = time.time()
    print('消耗的时间：', end_time - start_time)


if __name__ == '__main__':
    main()
