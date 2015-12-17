"""
    Test Build          tb_tc_hello_world_20120708185035
    Local Path          /apsarapangu/disk1/haowei.yao/workspace/atest_dev/atest_1_1/lib/atest/test/t/tc_hello_world.py
    Start Time          2012-07-08 18:50:36
    Stop Time           2012-07-08 18:50:36
    Duration            0.029 seconds
    Test Parameters
    Results
        F hello_world
          AssertionError: Hello, world!
    Statistics
        Passed=0 Failed=1 Canceled=0 Aborted=0
"""

class TestResult(object):
    separator1 = '=' * 70
    separator2 = '-' * 70

    def __init__(self,stream=None):
        self.stream = stream

        self.testsNo = 0

        self.successes = []
        self.failures = []
        self.errors = []
        self.cancles = []

        self._previousDriver = None
        self._currentDriver = None

        self.startTime = None
        self.stopTime = None
        self.timeTaken = 0
        self.results = []

    def startTestRun(self):
        """Called once before any tests are executed.
        See startTest for a method called before each test.
        """

    def stopTestRun(self):
        """Called once after all tests are executed.
        See stopTest for a method called after each test.
        """

    def startTest(self, test):
        """Called when the given test is about to be run"""
        self.stream.write(str(test))
        self.stream.write(" Start... \n")
        self.stream.flush()

    def stopTest(self, test):
        """Called when the given test has been run"""
        self.stream.write(str(test))
        self.stream.write("  End... \n")
        self.stream.flush()

    def addSuccess(self, test):
        "Called when a test has completed successfully"
        self.testsNo += 1
        self.stream.write("Success\n")
        self.successes.append((test, ''))

    def addFailure(self, test, err):
        self.testsNo += 1
        self.stream.write("Failure\n")
        self.failures.append((test, self._exc_info_to_string(err, test)))

    def addError(self, test, err):
        self.testsNo += 1
        self.stream.write("Error\n")
        self.failures.append((test, self._exc_info_to_string(err, test)))

    def writeStream(self, stream):
        self.stream.write(stream)
        self.stream.write('\n')

    def _exc_info_to_string(self, err, test):
        return str(err)

    def wasSuccessful(self):
        "Tells whether or not this result was a success"
        return len(self.failures) == 0

    def printResults(self):
        self.stream.write('\n')
        self.stream.write("Ran %d test%s in %.3fs\n" %
                            (self.testsNo, self.testsNo != 1 and "s" or "", self.timeTaken))
        self.printResultList('Passed', self.successes)
        self.printResultList('Failed', self.failures)
        self.printResultList('Aborted', self.errors)
        self.stream.write('\n')


    def printResultList(self, flavour, errors):
        for test, err in errors:
            self.stream.write(self.separator1)
            self.stream.write('\n')
            self.stream.write("%s: %s" % (flavour,test.name))
            self.stream.write('\n')
            self.stream.write(self.separator2)
            self.stream.write('\n')
            self.stream.write("%s" % err)
            self.stream.write('\n')
