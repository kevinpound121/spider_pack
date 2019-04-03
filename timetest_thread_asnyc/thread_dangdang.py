import requests
import threading
from queue import Queue
import time
import pandas as pd
from pyquery import PyQuery as pq


url_queue = Queue()
request_queue = Queue()
data_list = []


def set_url():
    for i in range(1, 51):
        url = 'http://bang.dangdang.com/books/bestsellers/1-{}'.format(i)
        url_queue.put(url) 


def get_request():
    while True:
        url = url_queue.get()
        res = requests.get(url)
        result = res.text
        doc = pq(result)
        # 生成pq对象，可迭代
        items = doc('.bang_list').children().items()
        request_queue.put(items)
        url_queue.task_done()


def parser_data():
    while True:
        items = request_queue.get()
        for i in items:
            rank = i('.list_num').text().strip('.')
            name = i('.name a').text()
            commments = i('.star a').text().strip('条评论')
            # eq指定第几个元素
            author = i('.publisher_info a').eq(0).text()
            publisher = i('.publisher_info a').eq(2).text() if len(i('.publisher_info a').eq(2).text()) >= 2 else ''
            data_list.append([rank, name, commments, author, publisher])
        request_queue.task_done()


def main():    
    thread_list = []
    t_set_url = threading.Thread(target=set_url)
    thread_list.append(t_set_url)

    for i in range(10):
        t_getrequest = threading.Thread(target=get_request)
        thread_list.append(t_getrequest)
    
    for i in range(5):
        t_parserdata = threading.Thread(target=parser_data)
        thread_list.append(t_parserdata)
    
    for task in thread_list:
        task.setDaemon(True)
        task.start()

    for q in [url_queue, request_queue]:
        q.join()
    
    df = pd.DataFrame(data_list, columns=['rank', 'name', 'comments', 'author', 'publisher'])
    df.to_csv('./dangdang-top-thread.csv', index=False, encoding='utf-8-sig')


if __name__ == '__main__':
    t1 = time.time()
    main()
    t2 = time.time()
    print('使用多线程的时间是：%s' %(t2-t1))
