import sys
import os
import loader, runner

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
    def usageExit(self, msg=None):
        if msg:
            print msg
        sys.exit(2)

    def parseArgs(self, argv):
        print 'parse args...'

    def createTests(self):
        print 'create tests...'

    def runTests(self):
        print 'print run tests...'

if __name__=="__main__":
    TestProgram(argv=sys.argv)
