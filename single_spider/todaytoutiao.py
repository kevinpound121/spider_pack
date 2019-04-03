import requests
from urllib.parse import urlencode
import json
from bs4 import BeautifulSoup
import re
import codecs


# 获取索引页
def getPageIndex(offset,keyword):
    key = {
        "offset": offset,
        "format": "json",
        "keyword": keyword,
        "autoload": "true",
        "count": 20,
        "cur_tab": 1,
        "from": "search_tab",
    }
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
        "method": "GET",
    }
    # print(urlencode(key))
    url = "https://www.toutiao.com/search_content/?"+urlencode(key)
    res = requests.get(url,headers = headers,timeout = 10)
    if res.status_code == 200:
        return res.text.encode('utf-8')
    return 'Bad Requests'





# 提取内容页链接
def parsePageIndex(html):
    # json.loads出来以后是一个对象，即key-value形式
    link = json.loads(html)
    # 遍历获取对象中名为data的字典
    for item in link.get("data"):
        # 确保article_url在该对象中，没有的话就跳过这一个 
        if "article_url" in item.keys():
            # print(item.get('article_url'))
            yield item.get('article_url')





# 获取内容页
def getPageDetail(link):
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
        "authority": "www.toutiao.com",
        "method":"GET"
    }
    res = requests.get(link,headers = headers,timeout = 5)
    if res.status_code == 200:
        return res.text




# 解析内容页
def getPageItem(html):    
    soup = BeautifulSoup(html,"lxml")
    # soup.select()返回的对象是一个list，所以需要用列表的方法取值 
    title = soup.select('title')[0].get_text()
    print(title)
    pattern = re.compile('''gallery: JSON.parse\("(.*?)"\),''',re.S)
    # 此时还是正则对象，没有被解析出来，不能使用re.sub(),也不能用codecs
    result = re.search(pattern,html)
    # 确保result数据是可以抓到的内容
    if result != None:
    #     # group以后正则对象变成了字符串，group(1)只提取(.*?)里的内容 
        content = result.group(1)
        # 去除多余斜杠
        content = codecs.decode(content,'unicode_escape')
        # 将字符串转换为json对象，方便提取内容
        a = json.loads(content)
        print(a)


        
        # 转化完变成字符串，但是无法用json.loads()转化为对象
        # a = re.sub(r"\\","",result["imgList"])
        # # print(result["imgList"])
        # url = json.loads(a)
        # print(type(a))
        # print(a)
    
            





def main():
    html = getPageIndex(0,'街拍')
    for i in parsePageIndex(html):
        content = getPageDetail(i)
        getPageItem(content)
if __name__ == '__main__':
    main()