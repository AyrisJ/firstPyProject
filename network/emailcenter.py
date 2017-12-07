# coding=utf-8
import smtplib
from email.mime.text import MIMEText
from email.header import Header


def send_email():
    smtp=smtplib.SMTP()
    try:
        smtp.connect("smtp.sina.com")
        smtp.login("asrasmiao@sina.com","xxxxxxx")

        subject="测试Python发送邮件"
        content="hello,python!中文结尾"
        mail_from="asrasmiao@sina.com"
        mail_to="fly_damwld@163.com"

        msg = MIMEText(content, "plain", _charset='utf-8')
        msg['Subject'] = Header(subject, 'utf-8')
        msg["From"] = mail_from

        smtp.sendmail(mail_from,mail_to,msg.as_string())
    except Exception as e:
        print e
    smtp.quit()


send_email()




