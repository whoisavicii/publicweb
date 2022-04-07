#coding=utf-8

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import smtplib
import os
import time
import csv



os.system('masscan -iL ip.txt -p1-65535  -oL masscan.txt --rate=20000')

while True:
    if os.path.exists("masscan.txt"):
        break
    else:
        time.sleep(1)
if os.path.getsize("masscan.txt") == 0:
    exit()
else :
    masscanfile = open("masscan.txt", "r")
    masscanfile.seek(0)
    for line in masscanfile:
        if line.startswith("#"):
            continue
        if line.startswith("open"):
            line = line.split(" ")
            print(line[3]+":"+line[2])
            with open("masscanconvert.txt", "a") as f:
                f.write(line[3]+":"+line[2]+"\n")
                f.close()
    masscanfile.close()
if os.path.exists("masscan.txt"):
    os.system('./httpx -l masscanconvert.txt -nc -status-code -title -silent -fr -csv -o httpxresult.csv')
    os.remove("masscan.txt")
else:
    exit()
with open('httpxresult.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    with open('互联网暴露面探测结果.csv', 'w', encoding='utf-8', newline='') as f1:
        writer = csv.writer(f1)
        writer.writerow(['序号', '系统', 'url', '标题', '服务', 'ip', '长度', '状态码', '位置','重定向后的url', '是否已报备安全团队', '是否进行关闭', '是否设置白名单', '无法设置白名单的原因', '备注'])
        i = 0
        for row in reader:
            url = row[8]
            title = row[11]
            webserver = row[13]
            host = row[17]
            contentlength = row[18]
            statuscode = row[20]
            finalurl = row[32]
            location = row[10]
            writer.writerow([i, '', url, title, webserver, host, contentlength, statuscode, location,finalurl, '', '', '', '', '', ''])
            i += 1          
os.remove('httpxresult.csv')
while True:
    if os.path.exists("masscanconvert.txt"):
        break
    else:
        time.sleep(1)
file = '互联网暴露面探测结果.csv' #附件路径
send_user = '*****@qq.com'   #发件人
password = '****'   #授权码/密码
receive_users = '****@qq.com'   #收件人，可为list
subject = '互联网暴露面web探测结果'  #邮件主题
email_text = '互联网暴露面web探测结果'   #邮件正文
server_address = 'smtp.qq.com'   #服务器地址
mail_type = '1'    #邮件类型
#构造一个邮件体：正文 附件
msg = MIMEMultipart()
msg['Subject']=subject    #主题
msg['From']=send_user      #发件人
msg['To']=receive_users           #收件人
#构建正文
part_text=MIMEText(email_text)
msg.attach(part_text)             #把正文加到邮件体里面去
#构建邮件附件
#file = file           #获取文件路径
part_attach1 = MIMEApplication(open(file,'rb').read())   #打开附件
part_attach1.add_header('Content-Disposition','attachment',filename=file) #为附件命名
msg.attach(part_attach1)   #添加附件
# 发送邮件 SMTP
smtp= smtplib.SMTP(server_address,25)  # 连接服务器，SMTP_SSL是安全传输
smtp.login(send_user, password)
smtp.sendmail(send_user, receive_users, msg.as_string())  # 发送邮件
print('邮件发送成功！')

