import requests
import re
from pymongo import MongoClient
import threading
from queue import Queue

conn = MongoClient('127.0.0.1', 27017)
db = conn.qiubai
db_article = db.article

base_url = 'https://www.qiushibaike.com/8hr/page/{}/'
headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"}
# 创建队列
url_queue = Queue()
res_queue = Queue()
data_queue = Queue()


def get_url(offset):
    for i in range(1, offset):
        url_queue.put(base_url.format(i))
    

def get_data():
    while True:
        print('正在抓取页面信息...')
        url = url_queue.get()
        print(url)
        res = requests.get(url, headers=headers)
        # 此处decode，默认为utf-8的模式
        content = res.content.decode()
        res_queue.put(content)
        print('抓取完毕...')
        url_queue.task_done()


def data_clean():
    while True:
        print('提取数据开始...')
        data = res_queue.get()
        # 构建正则
        regex = '<h2>(.*?)</h2>.*?<div class="content">.*?<span>(.*?)</span>.*?<i class="number">(\d+)</i>'
        # 加上re.S让点可以匹配空格换行
        pattern = re.compile(regex, re.S)
        data_raw = re.findall(pattern, data)
        content_list = []
        for item in data_raw:
            if int(item[2]) > 2000:
                data_dict = {}
                # 去除空格空行
                nick_name = item[0].strip()
                article1 = item[1].strip()
                # 去除<br/>
                article2 = re.sub('<br/>', '', article1)
                data_dict['nick_name'] = nick_name
                data_dict['article2'] = article2
                data_dict['like_num'] = item[2]
                content_list.append(data_dict)
        print(content_list)
        # data_queue.put(content_list)
        print('数据提取完毕...')
        res_queue.task_done()
                # 生成器输出的是元组
                # yield nick_name, article2, item[2]


def insert_mongo(data_gen):
    data_list = []
    for item in data_gen:
        data_insert = {
            'username': item[0],
            'article': item[1],
            'like': item[2],
        }
        data_list.append(data_insert)
    db_article.insert(data_list)


# def save_text(data_gen):
#     with open('./data/qiubai.txt', 'a', encoding='utf-8') as f:


if __name__ == '__main__':
    # 创建线程队列
    thread_list = []
    # 在给线程传参的时候，需要注意参数的写法，按照元组的方式传入6
    t_url = threading.Thread(target=get_url, args=(10,))
    thread_list.append(t_url)
    for i in range(20):
        t_get_data = threading.Thread(target=get_data)
        thread_list.append(t_get_data)
    for i in range(2):
        t_data_clean = threading.Thread(target=data_clean)
        thread_list.append(t_data_clean)
    # 开始运行线程队列
    for t in thread_list:
        t.setDaemon(True)
        t.start()
    # 队列阻塞，程序是否运行，依据的是队列里还有没有内容
    for q in [url_queue, res_queue, data_queue]:
        q.join()
    
    print('主程序结束')



    
