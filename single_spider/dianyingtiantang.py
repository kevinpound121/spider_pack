import requests
import re
import json
import csv
from requests.packages import urllib3

def get_download_page(url):
    response = requests.get('http://www.dytt8.net' + str(url), verify=False)
    response.encoding = 'gb2312'
    res = response.text
    # print(response.text)
    pattern = re.compile(
        '<div class="title_all.*?#07519a>(.*?)\s*</font>.*?发布时间：\s*(.*?)\s*<tr>.*?<img.*?src="(.*?)".*?<td style="WORD-WRAP: break-word".*?href="(.*?)"',
        re.S)
    # findall不能使用groups()
    result = re.search(pattern, res)
    if result != None:
        a = result.groups()
        return {
            "name": a[0],
            "time": a[1],
            # "poster":a[2],
            "downLoadLink": a[3]
        }
    else:
        return {
            'name':'none',
            'time':'none',
            'downLoadLink':'none',
        }


def get_list_page(arg):
    response = requests.get(
        'http://www.dytt8.net/html/gndy/dyzz/list_23_%s.html' % (arg + 1), verify=False)
    response.encoding = 'gb2312'
    result = response.text
    pattern = re.compile('<td height="26">.*?<a href="(.*?)" class="ulink">',
                         re.S)
    a = re.findall(pattern, result)
    # print(a)
    return a


def main():
    urllib3.disable_warnings()
    response = requests.get('http://www.dytt8.net/html/gndy/dyzz/index.html', verify=False)
    response.encoding = 'gb2312'
    result = response.text
    pattern = re.compile('共(\d*?)页', re.S)
    a = re.search(pattern, result)
    # group返回所有内容，groups返回括号内的内容
    pageNum = a.groups()[0]
    headers = ['电影名称', '上映时间', '下载链接']
    rows = []
    with open(r'./data/dytt_new.csv', 'a', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
    for i in range(int(pageNum)):
        linkSet = get_list_page(i)
        for item in linkSet:
            content = get_download_page(item)
            tup = (content['name'], content['time'], content['downLoadLink'])
            print(tup)
            rows.append(tup)
            if len(rows) > 500:
                # 编码格式采用utf-8-sig，避免中文乱码，也避免无法编码
                with open(r'./data/dytt_new.csv', 'a', encoding='utf-8-sig', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerows(rows)
                rows = []
    print('done')


if __name__ == '__main__':
    main()
