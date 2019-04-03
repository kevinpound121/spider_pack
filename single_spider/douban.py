import csv
import json
import requests

url = 'https://movie.douban.com/j/search_subjects?type=movie&tag=%E7%83%AD%E9%97%A8&page_limit=50&page_start=0'

headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Cookie': 'bid=QhdOsS_Jndw; gr_user_id=6f025d84-0ea0-4fb4-adb6-0017b43509eb; _vwo_uuid_v2=D8C860B4586657BE09AB411294899E4BD|923f4b4542158d6f0328ba1a4a1707a1; ll="118281"; viewed="26933281_26265544_26941639_26285406_3354490_3268399"; douban-fav-remind=1; __utmz=30149280.1541597098.6.4.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; ap_v=0,6.0; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1542436981%2C%22https%3A%2F%2Fwww.baidu.com%2Fs%3Fwd%3Ddouban%22%5D; _pk_ses.100001.4cf6=*; __utma=30149280.790187820.1538967134.1541597098.1542436981.7; __utmb=30149280.0.10.1542436981; __utmc=30149280; __utma=223695111.17480310.1541597098.1541597098.1542436981.2; __utmc=223695111; __utmz=223695111.1542436981.2.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic|utmctr=douban; __utmt=1; _pk_id.100001.4cf6=9bcb3188f9b00063.1541597097.2.1542436994.1541597097.; __utmb=223695111.2.10.1542436981',
    'Host': 'movie.douban.com',
    'Referer': 'https://movie.douban.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}


def get_data(url, headers):
    res = requests.get(url, headers=headers)
    res.encoding = 'utf-8'
    # print(res.content)
    data = json.loads(res.content)
    # print(data)
    header = ['电影名称', '电影评分', '信息页', '海报']
    rows = []
    for i in data['subjects']:
        tup = (i['title'], i['rate'], i['url'], i['cover'])
        rows.append(tup)
    # print(rows)
    return header, rows


def save_data(header, rows):    
    with open('./data/douban_movie.csv', 'w', encoding='gbk', newline='') as f:
        # 写excel
        writer = csv.writer(f, dialect='excel')
        writer.writerow(headers)
        writer.writerows(rows)
        # 写文本
        # for item in data['subjects']:
        #     f.write(str(item) + '\n')
        print('done')


def main():
    data = get_data(url=url, headers=headers)
    header = data[0]
    rows = data[1]
    save_data(header, rows)


if __name__ == '__main__':
    main()
