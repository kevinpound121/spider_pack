import requests
from bs4 import BeautifulSoup
import json


def get_page(url):
    headers = {
        "Host":
        "maoyan.com",
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
        "Connection":
        "close",
        "Cookie":
        "__mta=219117478.1537361432414.1537422009396.1537422078724.11; uuid_n_v=v1; uuid=968F51F0BC0A11E8B67057A7AC9C8D51FC6C1D94D8D745CCAEDDEE12E1C617DD; _csrf=2f8a67696966b88bc0d9b5ce9effd3d33ac8347b11796cd8a854a4a0cc1a6e29; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; _lxsdk_cuid=165f1e1cdcdc8-0c5a2c7cef8133-8383268-1fa400-165f1e1cdcfc8; _lxsdk=968F51F0BC0A11E8B67057A7AC9C8D51FC6C1D94D8D745CCAEDDEE12E1C617DD; __mta=219117478.1537361432414.1537361434050.1537361438507.3; _lxsdk_s=165f57c2e83-e15-766-cbd%7C%7C8"
    }
    res = requests.get(url, headers=headers)
    print(res.status_code)

    if res.status_code == 200:
        return res.text
    else:
        return "Bad request"


def parse_page(html):
    indexList = []
    imgList = []
    nameList = []
    actorList = []
    timeList = []
    scoreList = []
    soup = BeautifulSoup(html, 'lxml')
    content = soup.find_all('dd')
    print(content)
    for item in content:
        index = item.find('i', class_='board-index')
        indexList.append(index.get_text())
        img = item.find('img', class_='board-img')
        # print(img)
        imgList.append(img.get('data-src'))
        name = item.find('p', class_='name')
        nameList.append(name.get_text())
        actor = item.find('p', class_='star')
        actorList.append(actor.get_text().strip()[3:])
        time = item.find('p', class_='releasetime')
        timeList.append(time.get_text()[5:])
        score = item.find('p', class_='score')
        scoreList.append(score.get_text())
    # print(indexList,imgList,actorList,timeList,scoreList)
    for i in range(len(content)):
        yield {
            "电影排名": indexList[i],
            "电影名称": nameList[i],
            "电影海报": imgList[i],
            "电影主演": actorList[i],
            "上映时间": timeList[i],
            "电影评分": scoreList[i]
        }


def writeToFile(content):
    with open('maoYanTop100.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')


def main(arg):
    url = 'http://maoyan.com/board/4?offset=' + str(arg)
    html = get_page(url)
    for item in parse_page(html):
        print(item)
        writeToFile(item)

    # print(html)


if __name__ == '__main__':
    for i in range(10):
        main(i * 10)
