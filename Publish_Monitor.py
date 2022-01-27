# coding:utf-8
import requests
import time
import xlwt

# 代码分别为 [大连,营口,盘锦,深圳,东莞]
city_list = [210200, 210800, 211100, 440300, 441900]
json_data = []
now = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
filename = now + '.xls'

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36 Edg/97.0.1072.69'
}

for city in city_list:
    d = {'AreaID': city, 'MNName': '', 'RiverID': '', 'PageIndex': '-1', 'PageSize': '60', 'action': 'getRealDatas'}
    r = requests.post(url="http://106.37.208.243:8068/GJZ/Ajax/Publish.ashx", data=d, headers=header).json()
    json_data = json_data + r['tbody']
workbook = xlwt.Workbook()
sheet = workbook.add_sheet('sheet0', cell_overwrite_ok=True)

head_list = ['省份', '流域', '断面名称', '时间', '水质类别', '水温(℃)',
             'PH(无量纲)', '解氧(mg/L)', '电导率(μS/cm)', '浊度(NTU)', '高锰酸盐指数(mg/L)', '氨氮(mg/L)',
             '总磷(mg/L)', '总氮(mg/L)', '叶绿素(mg/L)', '藻密度(cells/L)', '站点情况']
for i in range(0, len(head_list)):
    sheet.write(0, i, head_list[i])

def writeExcel(excelPath, row, list):
    for i in range(0, len(list)):
        sheet.write(i + 1, row, list[i])

data_list = [[] for i in range(17)]
for i in range(0, len(json_data)):
    for j in range(0, 17):
        if (json_data[i][j] == None):
            data_list[j].append("None")
        elif (len(json_data[i][j]) > 15):
            data_list[j].append(json_data[i][j].split('>')[1][:-6])
        else:
            data_list[j].append(json_data[i][j])

for i in range(0, 17):
    writeExcel(filename, i, data_list[i])
workbook.save(filename)
print('数据获取结束，查看->'+filename)
