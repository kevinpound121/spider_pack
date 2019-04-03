import requests
from requests.exceptions import ConnectionError, Timeout, HTTPError
from fake_useragent import UserAgent
import browsercookie
from pyquery import PyQuery as pq
import pandas as pd


class LandChina:

    def __init__(self):
        self.url = 'http://www.landchina.com/default.aspx?tabid=261'
        self.headers = {
            'User-Agent': UserAgent().random,
            'Host': 'www.landchina.com',
            'Origin': 'http: // www.landchina.com',
            'Referer': 'http: // www.landchina.com / default.aspx?tabid = 261'
        }
        self.cookiesjar = browsercookie.chrome()
        self.end_page = 194  # 爬取多少页数据,共194页
        self.data_list = []  # 数据列表
        self.columns = ['number', 'area', 'title', 'type', 'publish_time', 'create_time', 'url']  # csv文件中按这个顺序写入

    def get_post_data(self, start_date, end_date, page):
        '''
        获取post请求的form_data数据
        :return: post_data 数据字典
        '''
        try:
            res = requests.get(self.url, headers=self.headers, cookies=self.cookiesjar)
            if res.status_code == 200:
                html = res.text
                # print(html)
            doc = pq(html)
            post_data = {}
            # post_data['TAB_QueryConditionItem'] = doc('#TAB_QueryConditionItem227').attr('value')
            TAB_ConditionItem = doc('#TAB_QueryConditionItem268').attr('value')
            post_data['TAB_QueryConditionItem'] = TAB_ConditionItem
            TAB_Sort = doc('#TAB_QuerySort0').attr('value')
            post_data['TAB_QuerySortItemList'] = TAB_Sort
            post_data['TAB_QuerySubmitOrderData'] = TAB_Sort
            post_data['__EVENTVALIDATION '] = doc('#__EVENTVALIDATION ').attr('value')
            post_data['__VIEWSTATE '] = doc('#__VIEWSTATE ').attr('value')
            post_data['TAB_QuerySubmitOrderData'] = doc('#TAB_QuerySubmitOrderData').attr('value')
            post_data['TAB_QuerySubmitConditionData'] = TAB_ConditionItem + str(start_date) + '~' + str(end_date)
            post_data['TAB_QuerySubmitPagerData'] = str(page)
            # print(post_data)
            return post_data

        except (ConnectionError, Timeout, HTTPError) as e:
            print('获取post_data数据失败', e)

    def get_detial_info(self, start_date, end_date, page):
        '''
        获取详细信息
        :return: None
        '''
        try:
            post_data = self.get_post_data(start_date, end_date, page)
            res = requests.post(self.url, headers=self.headers, cookies=self.cookiesjar, data=post_data)
            if res.status_code == 200:
                html = res.text
                # print(html)

            doc = pq(html)
            items = doc.find('#TAB_contentTable tr:gt(0)').items()
            for i in items:
                d = {}
                d['number'] = i('td:nth-child(1)').text()
                d['area'] = i('td:nth-child(2)').text()
                d['title'] = i('td:nth-child(3) a span').text()
                d['url'] = 'http://www.landchina.com' + i('td:nth-child(3) a').attr('href')
                d['type'] = i('td:nth-child(4)').text()
                d['publish_time'] = i('td:nth-child(5)').text()
                d['create_time'] = i('td:nth-child(6)').text()
                if d.get('area') in ['广州市本级', '荔湾区', '越秀区', '海珠区', '天河区', '白云区', '黄埔区', '番禺区', '花都区', '南沙区', '萝岗区',
                                     '增城市', '从化市']:
                    self.data_list.append(d)
            print(self.data_list)

        except (ConnectionError, Timeout, HTTPError) as e:
            print('获取详细信息失败', e)

    def run_spider(self, start_date, end_date):
        for i in range(1, self.end_page):
            print('正在抓取第{}页'.format(i))
            self.get_detial_info(start_date, end_date, i)
        # 保存到xls文件
        df = pd.DataFrame(self.data_list)
        df.to_excel('./data.xls', index=False, columns=self.columns)
        print('保存到xls文件')


if __name__ == '__main__':
    try:
        landchina = LandChina()
        landchina.run_spider('2019-1-1', '2019-3-8')
    except Exception as e:
        print(e)
