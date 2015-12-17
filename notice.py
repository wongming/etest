import smtplib
from email.mime.text import MIMEText

class TestNotice(object):
    def __init__(self):
        self.smtp = smtplib.SMTP()
        self.mail_host = 'smtp.qq.com'
        self.mail_user = "byonecry"
        self.mail_from = 'byonecry@qq.com'
        self.mail_pwd = "xxx"
    def sendEmailNotice(self, result):
        msg = MIMEText('<html><h1>hello</h1></html>','html','utf-8')
        msg['Subject'] = result.description
        msg['From'] = self.mail_from
        msg['To'] = result.emailList
        self.smtp.connect(self.mail_host)
        self.smtp.login(self.mail_user, self.mail_pwd)
        self.smtp.sendmail(self.mail_from, result.emailList.split(','), msg.as_string())
        self.smtp.quit()

if __name__=="__main__":
    TestNotice().sendEmailNotice2('ss')
