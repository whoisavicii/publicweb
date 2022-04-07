#处理csv表格数据
import csv
from time import sleep
import requests
import os

print('----------Nessus端口扫描结果转换成url并调用httpx探测----------')
file = input("将nessus端口扫描结果拖进来") #输入文件名
#处理csv表格数据，第五列数据为ip，第七列数据为port，组合成http://ip:port并保存到新的txt文件中，ip不等于'Host'，port不等于'Port'
with open(file, 'r', encoding='utf-8') as f: #打开文件
    reader = csv.reader(f) #读取文件
    with open('url.txt', 'w', encoding='utf-8', newline='') as f1: #打开新文件
        writer = csv.writer(f1) #写入新文件
        for row in reader:
            ip = row[4] #读取第五列数据
            port = row[6] #读取第七列数据
            if ip != 'Host' and port != 'Port':
                url = 'http://' + ip + ':' + port
                writer.writerow([url])
print('已成功提取nessus扫描报告中的ip端口')
sleep(1)
print('正在使用httpx进行请求')


os.system(r'.\httpx.exe -l .\url.txt -nc -status-code -title -silent -fr -csv -o .\httpxresult.csv')
#删除url.txt文件
os.remove('url.txt')
print('httpx执行完毕，正在整理csv文件')
#读取httpxresult.csv文件
#url为第10列数据，title为第13列数据，webserver为第15列数据，host为第19列数据，contentlength为第20列数据，statuscode为第21列数据，finalurl为第33列数据
#将url, title, webserver, host, contentlength, statuscode, finalurl写入新的new.csv文件中
#设置csv文件的列名第一列为序号，第二列为系统，第三列为url，第四列为title，第五列为webserver，第六列为host，第七列为contentlength，第八列为statuscode，第九列为finalurl，第十列为是否已报备安全团队，第十二列为是否进行关闭，第十三列为是否设置白名单，第十四列为无法设置白名单的原因，第十五列为备注
with open('httpxresult.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    with open('new.csv', 'w', encoding='utf-8', newline='') as f1:
        writer = csv.writer(f1)
        writer.writerow(['序号', '系统', 'url', '标题', 'webserver', 'host', '长度', '状态码', 'finalurl', '是否已报备安全团队', '是否进行关闭', '是否设置白名单', '无法设置白名单的原因', '备注'])
        i = 1
        for row in reader:
            url = row[10]
            title = row[13]
            webserver = row[15]
            host = row[19]
            contentlength = row[20]
            statuscode = row[22]
            finalurl = row[33]
            writer.writerow([i, '', url, title, webserver, host, contentlength, statuscode, finalurl, '', '', '', '', '', ''])
            i += 1  
           
#删除httpxresult.csv文件
os.remove('httpxresult.csv')

print('----------web探测完成----------')
print('请查看当前的web探测结果.csv')
sleep(10)
