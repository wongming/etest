from setuptools import setup, find_packages
import os,sys
import shutil
import traceback

setup(
    name = 'stest',
    version = "1.0.0",
    packages = find_packages(),
    package_data = {'': ['*.txt',
                         '*.html',
                         '*.md',
                         ]
    },
    entry_points = {
        'console_scripts': [
            'stest = stest:main',
        ]
    }
 )
try:
    conf_path = os.path.expanduser('~/.stest')
    if not os.path.exists(conf_path):
        os.mkdir(conf_path)
    driver_path = os.path.join(conf_path, 'driver')
    if not os.path.exists(driver_path):
        os.mkdir(driver_path)
    conf_file = os.path.join(conf_path,'stest.conf')
    if not os.path.exists(conf_file):
        shutil.copyfile('./stest/stest.conf.template', conf_file)
    email_template_file = os.path.join(conf_path, 'EmailTemplate.html')
    if not os.path.exists(email_template_file):
        shutil.copyfile('./stest/EmailTemplate.html',email_template_file)
    #替换文件中的~
    
except:
    print 'Conf resource processed error'
    traceback.print_exc()
    #print "Remove dir '~/.stest' and try again"
