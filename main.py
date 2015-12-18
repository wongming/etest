import sys
import os
import loader, runner
import notice
"""
    Running tests:

    Examples:
        stest -rt ts_xxx           - run tests from a driver
        stest -rt ts_xxx#tm_xxx    - run tests from a test method
        stest -rt ts_xxx           - run tests from a dir
        stest -rp xxx.plan.json    - run plan
"""
class TestProgram(object):
    def __init__(self, argv=None, testRunner=runner.defaultTestRunner, testLoader=loader.defaultTestLoader):
        self.testRunner = testRunner
        self.testLoader = testLoader
        #self.testRunner = runner.TextTestRunner
        if argv is None:
            argv = sys.argv
        self.parseArgs(argv)
        self.createTests()
        self.runTests()

    def usageExit(self, msg=None):
        if msg:
            print msg
        sys.exit(2)

    def parseArgs(self, argv):
        print 'parse args...'

    def createTests(self):
        print 'create tests...'
        #self.tests = self.testLoader.loadTestsFromFile('tc_d2')
        self.tests = self.testLoader.loadTestsFromDir('ts_lay1')

    def runTests(self):
        print 'print run tests...'
        self.result = self.testRunner.run(self.tests)
        self.result.description = 'SMDB Test Report from ATRS'
        self.result.emailList = '378406534@qq.com'
        import notice
        notice.TestNotice().sendEmailNotice(self.result)

if __name__=="__main__":
    TestProgram()
