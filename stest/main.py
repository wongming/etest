import sys
import os

from stest import loader, runner, notice

UsageInfo = """\
Usage: stest [options] [argv] [...]
options:
    -h, --help      Show this help message
    -v, --version   Show tool version info
    -c, --case      run test cases
    -p, --plan      run test plans
    -d, --driver    list dirvers
Examples:
        stest -c ts_xxx/tc_xxx     - run tests from a file
        stest -c ts_xxx/           - run tests from a dir
        stest -c ts_xxx#tm_xxx    - run tests from a test method of a file
        stest -p ts_xxx           - run plans of a dir
        stest -p xxx.plan.json    - run a plan from a file
"""
VersionInfo = 'stest version "1.0"'
class TestProgram(object):
    usage = UsageInfo
    version = VersionInfo
    def __init__(self, argv=None, testRunner=runner.defaultTestRunner, testLoader=loader.defaultTestLoader):
        self.testRunner = testRunner
        self.testLoader = testLoader
        #self.testRunner = runner.TextTestRunner
        self.target = None
        self.isCase = False
        self.isPlan = False
        self.plan = None
        self.tests =None
        if argv is None:
            argv = sys.argv[1:]
        self.parseArgs(argv)
        self.createTests()
        self.runTests()

    def usageExit(self, msg=None, version=False):
        #print 'stest::: usageExit...'
        if version:
            print self.version
        if msg:
            print msg
        if not version and not msg:
            print self.usage
        sys.exit(2)

    def parseArgs(self, argv):
        #print 'stest::: parseArgs...'
        import getopt
        long_opts = ["help", "version","case=", "plan=", "driver"]
        short_opts= "hHvc:p:d"
        if len(argv)==0:
            self.usageExit()
        try:
            options, args = getopt.getopt(argv, short_opts, long_opts)
            for opt, value in options:
                if opt in ('-h','-H','--help'):
                    self.usageExit()
                elif opt in ("-v","--version"):
                    self.usageExit(version=True)
                elif opt in ('--case','-c'):
                    self.isCase = True
                    if not os.path.exists(value):
                        self.usageExit("%s not found" % value)
                    self.target = os.path.abspath(value)
                elif opt in ('--plan','-p'):
                    self.isPlan = True
                    if not os.path.exists(value):
                        self.usageExit("%s not found" % value)
                    self.target =os.path.abspath(value)
                elif opt in ('-d', '--driver'):
                    self.usageExit("Drivers Contains Below:\n   " + self.testLoader.listDrivers())
        except getopt.error, msg:
            self.usageExit(msg)

    def createTests(self):
        #print 'stest::: create tests...'
        if self.isPlan:
            self.plan, self.tests = self.testLoader.loadTestsFromPlan(self.target)
        elif self.isCase:
            if os.path.isdir(self.target):
                self.tests = self.testLoader.loadTestsFromDir(self.target)
            if os.path.isfile(self.target):
                self.tests = self.testLoader.loadTestsFromFile(self.target)

    def runTests(self):
        #print 'stest::: print run tests...'
        self.result = self.testRunner.run(self.tests)
        if self.isPlan:
            self.result.description = 'Test Report of [%s] from ATRS' % self.plan['Plan Name']
            self.result.emailList = self.plan['Email List']
            import notice
            notice.TestNotice().sendEmailNotice(self.result)

run_exit = main = TestProgram

if __name__=="__main__":
    TestProgram()
