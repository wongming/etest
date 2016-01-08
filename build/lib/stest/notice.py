import os
import smtplib
from email.mime.text import MIMEText
import ConfigParser

__stest = True

class TestNotice(object):
    def __init__(self):
        self.smtp = smtplib.SMTP()
        conf = ConfigParser.ConfigParser()
        conf.read(os.path.expanduser('~/.stest/stest.conf'))
        self.mail_host = conf.get('notice','MailHost')
        self.mail_user = conf.get('notice','MailUser')
        self.mail_from = conf.get('notice','MailFrom')
        self.mail_pwd = conf.get('notice','MailPwd')
        self.emailTemplatePath = os.path.expanduser('~/.stest/EmailTemplate.html')
        if 'EmailTemplatePath' in conf.options('base'):
            self.emailTemplatePath = os.path.expanduser(conf.get('base','EmailTemplatePath'))

    def sendEmailNotice(self, result):
        template = file(self.emailTemplatePath).read()
        template = template.replace('$planName',result.description)
        template = template.replace('$emailList',result.emailList)
        template = template.replace('$duration','Total %s Seconds. ( %s -- %s )' % (result.timeTaken, result.startTime, result.stopTime))
        template = template.replace('$statistics','Passed: %i,  Failed: %i,  Aborted: %i' % (len(result.successes), len(result.failures), len(result.errors)))
        template = template.replace('$log',result.log.getvalue())
        results = []
        results.append('<table>')
        for item in result.results:
            results.append('<tr><td class="%s">%s</td><td>%s</td></tr>' % (item[1], item[1], item[0]))
            """
            if not item[1]=='Passed':
                results.append('<tr><td></td><td><pre class="error_info">')
                results.append('%s' % (item[2]))
                results.append('</pre></td></tr>')
            """
        results.append('</table>')
        template = template.replace('$results',''.join(results))
        msg = MIMEText(template, _subtype='html')
        msg['Subject'] = result.description
        msg['From'] = self.mail_from
        msg['To'] = result.emailList
        self.smtp.connect(self.mail_host)
        self.smtp.login(self.mail_user, self.mail_pwd)
        self.smtp.sendmail(self.mail_from, result.emailList.split(','), msg.as_string())
        self.smtp.quit()
