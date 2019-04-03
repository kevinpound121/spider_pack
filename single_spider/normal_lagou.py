import requests
import json
import time
import pymongo


conn = pymongo.MongoClient('localhost')
db = conn.lagou
db_JobInfo = db.JobInfo


def get_url(page_num):
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
        # 更改搜索页数，以及收缩关键词
        "first": " true",
        "pn": str(page_num),
        "kd": " python",
    }
    res = requests.get(base_url, headers=headers, params=params)
    html = res.text
    # 取回的数据是字符串，需要转化成json进行提取
    content = json.loads(html)
    if content.get('content'):
        # print(content)
        return content
    else:
        time.sleep(30)
        print('take a brake')
        return get_url(page_num)


def data_clean(raw_data):
    info_list = []
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
        info_list.append(info_dict)
    print(info_list)
    return info_list


def insert_mongo(info_list):
    for item in info_list:
        db_JobInfo.insert(item)


def main(page_num=1):
    for i in range(page_num):
        raw_data = get_url(i)
        info_list = data_clean(raw_data)
        insert_mongo(info_list)


if __name__ == '__main__':
    main(10)
