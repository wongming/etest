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
        template = file("/Users/wangming/workspace/etest/EmailTemplate.html").read()
        template = template.replace('$planName',result.description)
        template = template.replace('$emailList',result.emailList)
        template = template.replace('$duration','Total %s Seconds. ( %s -- %s )' % (result.timeTaken, result.startTime, result.stopTime))
        template = template.replace('$statistics','Passed: %i,  Failed: %i,  Aborted: %i' % (len(result.successes), len(result.failures), len(result.errors)))
        template = template.replace('$log','')
        results = []
        for item in result.results:
            results.append('<tr><td class="%s">%s</td><td>%s</td></tr>' % (item[1], item[1],item[0]))
        template = template.replace('$results',''.join(results))
        msg = MIMEText(template, _subtype='html')
        msg['Subject'] = result.description
        msg['From'] = self.mail_from
        msg['To'] = result.emailList
        self.smtp.connect(self.mail_host)
        self.smtp.login(self.mail_user, self.mail_pwd)
        self.smtp.sendmail(self.mail_from, result.emailList.split(','), msg.as_string())
        self.smtp.quit()

if __name__=="__main__":
    template = file("/Users/wangming/workspace/etest/EmailTemplate.html").read()
    print template.replace('$planName','result.description')
    print template
