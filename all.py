# coding:utf-8
import os
import time
import xlwt
import json

# 代码分别为 [大连,营口,盘锦,深圳,东莞]
city_list = [210200, 210800, 211100, 440300, 441900]
json_data = []
now = time.strftime("%Y-%m-%d--%H-%M-%S", time.localtime())
filename = now + '.xls'
file_list = os.listdir('.')
other = 0
for file in file_list:
    if file.endswith('.json') or file.endswith('.txt') and not file == 'all.txt':
        other = other + 1
if 'all.txt' not in file_list:
    print('没有all.txt,是否继续？')
    print('任意键继续，按"n"退出')
    # os.system('pause')
    if input() == 'n':
        print('程序结束')
        exit()
else:
    print('存在all.txt')
    line_list_left = []
    line_list_right = []

    with open('all.txt', encoding='utf-8', errors='ignore' 'r') as f:
        for i, line in enumerate(f):
            if '{' in line:
                line_list_left.append(i)
                # print(i+1)
    with open('all.txt', encoding='utf-8', errors='ignore' 'r') as f:
        for i, line in enumerate(f):
            if '}' in line:
                line_list_right.append(i)
                # print(i+1)


    def read_write_txt(file_name, row0, row1):
        with open(file_name, encoding='utf-8', errors='ignore') as f:
            f_write.write('{')
            f_write.write('\n')
            for i, line in enumerate(f):
                if i > row0 and i < row1:
                    f_write.write(line)
            f_write.write('}')
            f_write.write('\n')


    count = 0
    print('已将all.txt划分为：')
    for i, j in zip(line_list_left, line_list_right):
        # print(i,j)
        with open('all_' + str(count + 1) + '.txt', 'w', encoding='utf-8', errors='ignore') as f_write:
            read_write_txt('all.txt', i, j)
        print('all_' + str(count + 1) + '.txt')
        count = count + 1


if other == 0:
    file_list = os.listdir('.')
    # 读取所有json文件
    print('读取当前目录下所有json/txt文件，已读取到的有：')
    for file in file_list:
        if file.endswith('.json') or file.endswith('.txt'):
            if file == 'all.txt':
                continue
            print(file)
            with open(file,encoding='utf-8',errors='ignore') as file_data:
                data = json.load(file_data)
            json_data = json_data + data['tbody']
else :
    print('目录下包含all.txt之外的其他txt/json，是否将其包含进去？(y/n)')
    for file in file_list:
        if file.endswith('.json') or file.endswith('.txt') and not file == 'all.txt':
            print(file)
    if input() == 'y':
        file_list = os.listdir('.')
        # 读取所有json文件
        print('读取当前目录下所有json/txt文件，已读取到的有：')
        for file in file_list:
            if file.endswith('.json') or file.endswith('.txt'):
                if file == 'all.txt':
                    continue
                print(file)
                with open(file, encoding='utf-8', errors='ignore') as file_data:
                    data = json.load(file_data)
                json_data = json_data + data['tbody']
    # elif input() == 'n':
    else:
        file_list = os.listdir('.')
        # 读取所有json文件
        print('读取当前目录下所有json/txt文件，已读取到的有：')
        for file in file_list:
            if (file.endswith('.json') or file.endswith('.txt')) and file.startswith('all_'):
                if file == 'all.txt':
                    continue
                print(file)
                with open(file, encoding='utf-8', errors='ignore') as file_data:
                    data = json.load(file_data)
                json_data = json_data + data['tbody']
                os.remove(file)

# file_list = os.listdir('.')
# for file in file_list:
#     if file.startswith('all_'):
#         os.remove(file)


os.system('pause')

# with open('test.json',encoding='utf-8',errors='ignore') as file_data:
#     json_data = json.load(file_data)
# print(json_data['tbody'])

workbook = xlwt.Workbook()
sheet = workbook.add_sheet('sheet0', cell_overwrite_ok=True)

head_list = ['省份', '流域', '断面名称', '时间', '水质类别', '水温(℃)',
             'PH(无量纲)', '解氧(mg/L)', '电导率(μS/cm)', '浊度(NTU)', '高锰酸盐指数(mg/L)', '氨氮(mg/L)',
             '总磷(mg/L)', '总氮(mg/L)', '叶绿素(mg/L)', '藻密度(cells/L)', '站点情况']
for i in range(0, len(head_list)):
    sheet.write(0, i, head_list[i])

# 将列表row_list数据写到第row列 （从excel第二行开始写）
def write_excel(row, row_list):
    for i in range(0, len(row_list)):
        sheet.write(i + 1, row, row_list[i])


data_list = [[] for i in range(len(head_list))]
for i in range(0, len(json_data)):
    for j in range(0, len(head_list)):
        if json_data[i][j] == None:
            data_list[j].append("None")
        elif len(json_data[i][j]) > 15:
            data_list[j].append(json_data[i][j].split('>')[1][:-6])
        else:
            if j == 0:
                data_list[j].append(json_data[i][j] + '(' + json_data[i][j + 2].split(':')[1][:-9] + ')')
            else:
                data_list[j].append(json_data[i][j])

for i in range(0, len(head_list)):
    write_excel(i, data_list[i])
workbook.save(filename)
print('数据获取结束，查看->' + filename)
os.system("pause")