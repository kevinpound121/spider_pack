import requests
from lxml import etree
import time,re,random,xlrd,xlwt
from xlutils.copy import copy

url = "http://218.14.150.123/htmlaspx/tmsfw-jiangmen/hpms/ProjectInfoList.aspx"
i = 1 # 计数

def main():
    response = requests.get(url).content.decode('utf-8')
    html = etree.HTML(response)
    items = html.xpath("//td[@align='left']/a")
    "//td[@align='left']/a/u/text()"
    data = {}
    for item in items:
        uri = item.xpath("./@href")[0]
        # print(uri)
        data['楼盘名'] = item.xpath("./u/text()")[0]
        detail_uri = uri.replace('../../../htmlaspx/FUN_TMSFW_DETAILPROJECT.SOUTH?', '')
        detail_url = "http://218.14.150.123/htmlaspx/tmsfw-jiangmen/hpms/ProjectDetailsInfo.aspx?" + detail_uri
        # print(detail_url)
        data['楼盘url'] = detail_url
        # print(data)
        time.sleep(1)
        parse_detail(detail_url, data)

def parse_detail(url, data):
    response = requests.get(url).content.decode('utf-8')
    html = etree.HTML(response)
    data['项目名称'] = html.xpath("//span[@id='Project_XMMC']/text()")
    data['项目地址'] = html.xpath("//span[@id='Project_XMDZ']/text()")
    data['开发商'] = html.xpath("//span[@id='Project_KFQY_NAME']/text()")
    data['总建筑面积'] = html.xpath("//span[@id='Project_GHZJZMJ']/text()")
    data['资质证书编号'] = html.xpath("//span[@id='lblZZZS']/text()")
    data['核准预售套数'] = html.xpath("//span[@id='lblHZYSZTS']/text()")
    data['已售总套数'] = html.xpath("//span[@id='lblYSZTS']/text()")
    data['已售总面积'] = html.xpath("//span[@id='lblYSZMJ']/text()")
    data['楼盘销售部地址'] = html.xpath("//span[@id='Project_SLCDH']/text()")
    data['行政区划'] = html.xpath("//span[@id='lblSZQY']/text()")
    data['容积率'] = html.xpath("//span[@id='Project_RJL']/text()")
    data['资质等级'] = html.xpath("//span[@id='lblZZDJ']/text()")
    data['标准预售体积'] = html.xpath("//span[@id='lblHZYSZMJ']/text()")
    data['未售总套数'] = html.xpath("//span[@id='lblWSZTS']/text()")
    data['未售总面积'] = html.xpath("//span[@id='lblWSZMJ']/text()")
    data['楼盘销售部电话'] = html.xpath("//span[@id='Project_SLDH']/text()")
    for key,value in data.items():
        if value == []:
            data[key] = ''
        elif isinstance(value,list):
            data[key] = value[0]
    # print(data)
    # 判断有几个选择框
    nums = html.xpath("//input[@name='radiobuild']")
    # print(len(nums))
    if len(nums) > 1:
        for item in nums:
            bid = item.xpath('./@bid')[0]
            js_exeServerFun(bid,data)
    else:
        # print(nums)
        bid = nums[0].xpath('./@bid')[0]
        js_exeServerFun(bid,data)
    # exeServerFun(sMethod, CBuildTableV2_callback, strXDDir, this.sBuildCode, this.iBuildUnitType, this.iBuildTableType, this.iMinCellWidth, this.iMinTableWidth, this.sInstance, this.sWhere, this.bOnlyLoadValidRoom, this.sOperationCode,this.sWhere2);
    # exeServerFun("SouthDigital.Wsba2.CBuildTableV2.GetBuildHTMLEx",false,"../","123298",1,1,80,840,"g_oBuildTable"," 1=1",true,'','')

def js_exeServerFun(bid,data):
    # Xml = '<?xml version="1.0" encoding="utf-8" standalone="yes"?>\n<param funname="SouthDigital.Wsba2.CBuildTableV2.GetBuildHTMLEx">\n'
    # Xml = Xml + createParamXml(False)
    # Xml = Xml + createParamXml('123298')
    # Xml = Xml + createParamXml('1')
    # Xml = Xml + createParamXml("1")
    # Xml = Xml + createParamXml("80")
    # Xml = Xml + createParamXml("840")
    # Xml = Xml + createParamXml("g_oBuildTable")
    # Xml = Xml + createParamXml(" 1=1")
    # Xml = Xml + createParamXml(True)
    # Xml = Xml + createParamXml('')
    # Xml = Xml + createParamXml('')
    # Xml = Xml + "</param>\n";
    global i
    xml = "%3C?xml%20version=%221.0%22%20encoding=%22utf-8%22%20standalone=%22yes%22?%3E%0A%3Cparam%20funname=%22SouthDigital.Wsba2.CBuildTableV2.GetBuildHTMLEx%22%3E%0A%3Citem%3E../%3C/item%3E%0A%3Citem%3E{}%3C/item%3E%0A%3Citem%3E1%3C/item%3E%0A%3Citem%3E1%3C/item%3E%0A%3Citem%3E80%3C/item%3E%0A%3Citem%3E840%3C/item%3E%0A%3Citem%3Eg_oBuildTable%3C/item%3E%0A%3Citem%3E%201=1%3C/item%3E%0A%3Citem%3E1%3C/item%3E%0A%3Citem%3E%3C/item%3E%0A%3Citem%3E%3C/item%3E%0A%3C/param%3E%0A".format(bid)
    # print(xml)
    url = 'http://218.14.150.123/Common/Agents/ExeFunCommon.aspx?' + str(random.random()) + str(
        int(round(time.time() * 1000)))
    response = requests.post(url,data=xml).content.decode('utf-8')
    html = etree.HTML(response)
    houses = html.xpath('//table[@class="TB_Body"]//td')
    pcode = get_dcode(data['楼盘url'])

    for house in houses:
        # data['楼盘名'] = data['楼盘名']
        # data['楼盘url'] = data['楼盘url']
        data['房屋号'] = house.xpath('./u/text()')[0]
        data['房屋状态'] = get_house_state(house.xpath('./@style')[0])
        code = get_house_code(house.xpath("./u/@onclick")[0])
        data['房屋url'] ="http://218.14.150.123/htmlaspx/FUN_TMSFW_ROOMINFO.SOUTH?code={}&PCODE={}".format(code,pcode)
        i = i+1
        save_to_excel(i,data)
        print(data)

def get_dcode(url):
    regex = "code=(.*)"
    pattern = re.compile(regex, re.S)
    res = pattern.findall(url)[0]
    return res

def get_house_code(code_str):
    regex = "'(.*)'"
    pattern = re.compile(regex, re.S)
    res = pattern.findall(code_str)[0]
    return res

def get_house_state(state_str):
    state_color = {
        '可售':'#00FF00',
        '已预订':'#FD66FF',
        '已签约': '#FAB600',
        '已备案': '#74F9FB',
        '限制房产': 'red',
    }
    regex = "background-color:(.*);"
    pattern = re.compile(regex,re.S)
    res = pattern.findall(state_str)[0]
    # print(res)
    for key,value in state_color.items():
        # print(value)
        if res == value:
            # print(key,value)
            return key

def save_to_excel(i, data):
    # 如果没有xls文件则新建文件
    try:
        work = xlrd.open_workbook('./jiangmen.xls')
        # work = xlrd.open_workbook('.\\jiangmen.xls')
        workbook = copy(work)
        worksheet = workbook.get_sheet(0)
        # print(1)
    except Exception as e:
        # print(e)
        workbook = xlwt.Workbook(encoding='utf-8')
        worksheet = workbook.add_sheet('sheet1')

    finally:
        for index, key in enumerate(data):
            worksheet.write(0, index, label=key)
            worksheet.write(i, index, label=data[key])
        workbook.save('jiangmen.xls')

# def createParamXml(p):
#     sXml = ""
#     if (p != ''):
#         sVal = p;
#         if (isinstance(p, str)):
#             pass
#         elif (p == True):
#             sVal = "1";
#         elif (p == False):
#             sVal = "0";
#         sXml = "<item>" + XmlEncode(sVal + "") + "</item>\n";
#     return sXml
#
# def XmlEncode(text):  ##防代码注入
#     return text.replace('&', "&amp;").replace('<', "&lt;");

if __name__ == '__main__':

    main()
    # js_exeServerFun("123298",{'楼盘url':"http://218.14.150.123/htmlaspx/tmsfw-jiangmen/hpms/ProjectDetailsInfo.aspx?code=96076"})
