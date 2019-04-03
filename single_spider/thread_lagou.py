import requests
import json
import time
import pymongo
import threading
from queue import Queue

# init mongo
conn = pymongo.MongoClient('localhost')
db = conn.lagou
db_JobInfo = db.JobInfo

# create queue
params_queue = Queue()
data_queue = Queue()
db_queue = Queue()


def set_pagenum(page_num):
    print('设置页码')
    for i in range(page_num):
        params_queue.put(i+1)


def get_data():
    while True:
        page_num = params_queue.get()
        base_url = 'https://www.lagou.com/jobs/positionAjax.json?city=%E5%B9%BF%E5%B7%9E&needAddtionalResult=false'
        headers = {
            # 异步请求的时候需要注意请求头，要有referer等一些关键的因素
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput=',
            'Pragma': 'no-cache',
            'Origin': 'https://www.lagou.com',

        }
        params = {
            "first": " true",
            "pn": str(page_num),
            "kd": " python",
        }
        print('正在获取第{}页url'.format(page_num))
        res = requests.get(base_url, headers=headers, params=params)
        html = res.text
        print(len(html))
        # 取回的数据是字符串，需要转化成json进行提取
        content = json.loads(html)
        print(content)
        if content.get('content'):
            print('将url注入队列')
            data_queue.put(content)
            params_queue.task_done()
        else:
            # 将获取失败的链接重新推入队列
            time.sleep(30)
            params_queue.put(page_num)
            print('take a brake')
            params_queue.task_done()
            

def data_clean():
    print('数据清洗中')
    while True:
        raw_data = data_queue.get()
        detail = raw_data['content']['positionResult']['result']
        # print(detail[0]['salary'])
        for item in detail:
            # print(item)
            info_dict = {
                'companyShortName': item['companyShortName'],
                'companyFullName': item['companyFullName'],
                'businessZones': item['businessZones'],
                'companyLabelList': item['companyLabelList'],
                'companySize': item['companySize'],
                'createTime': item['createTime'],
                'district': item['district'],
                'education': item['education'],
                'financeStage': item['financeStage'],
                'firstType': item['firstType'],
                'industryLables': item['industryLables'],
                'positionAdvantage': item['positionAdvantage'],
                'positionName': item['positionName'],
                'salary': item['salary'],
                'secondType': item['secondType'],
                'stationname': item['stationname'],
                'subwayline': item['subwayline'],
                'thirdType': item['thirdType'],
                'workYear': item['workYear'],
                'companyId': item['companyId'],
                'latitude': item['latitude'],
                'longitude': item['longitude'],
                'positionId': item['positionId']
            }
            db_queue.put(info_dict)
        print('已注入一页信息')
        data_queue.task_done()


def insert_mongo():
    print('插入数据库')
    while True:       
        data = db_queue.get()
        db_JobInfo.insert(data)
        db_queue.task_done()



def main(page_num=1):
    thread_list = []
    # 设定页数
    t_set_pagenum = threading.Thread(target=set_pagenum, args=(page_num,))
    thread_list.append(t_set_pagenum)
    # 获取页面信息
    for i in range(20):
        t_getdata = threading.Thread(target=get_data)
        thread_list.append(t_getdata)  
    # 数据清洗
    for i in range(5):
        t_dataclean = threading.Thread(target=data_clean)
        thread_list.append(t_dataclean)
    # 录入数据库
    for i in range(2):
        t_insertdb = threading.Thread(target=insert_mongo)
        thread_list.append(t_insertdb)

    print('此时队列中任务数为：{}'.format(len(thread_list)))
    # 线程启动
    for task in thread_list:
        task.setDaemon(True)
        task.start()

    # 设置队列阻塞
    for q in [params_queue, data_queue, db_queue]:
        q.join()
    

if __name__ == '__main__':
    # main(10)
    set_pagenum(10)
    print('全部结束')

