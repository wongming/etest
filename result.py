class TestResult(object):
    separator1 = '=' * 70
    separator2 = '-' * 70

    def __init__(self,stream=None):
        self.stream = stream
        self.testsNo = 0
        self.failures = []
        self._previousDriver = None
        self._currentDriver = None

    def startTestRun(self):
        """Called once before any tests are executed.
        See startTest for a method called before each test.
        """
        pass

    def stopTestRun(self):
        """Called once after all tests are executed.
        See stopTest for a method called after each test.
        """

    def startTest(self, test):
        """Called when the given test is about to be run"""
        self.testsNo += 1
        self.stream.write(test.name)
        self.stream.write(" ... ")
        self.stream.flush()

    def stopTest(self, test):
        """Called when the given test has been run"""

    def addSuccess(self, test):
        "Called when a test has completed successfully"
        self.stream.writeln("Success")

    def addFailure(self, test, err):
        self.stream.writeln("Failure")
        self.failures.append((test, self._exc_info_to_string(err, test)))

    def _exc_info_to_string(self, err, test):
        return str(err)

    def wasSuccessful(self):
        "Tells whether or not this result was a success"
        return len(self.failures) == 0

    def printResults(self):
        self.stream.writeln()
        self.stream.writeln("Ran %d test%s in %.3fs" %
                            (testsNo, testsNo != 1 and "s" or "", timeTaken))
        self.printErrorList('Failure', self.failures)
        self.stream.writeln()


    def printResultList(self, flavour, errors):
        for test, err in errors:
            self.stream.writeln(self.separator1)
            self.stream.writeln("%s: %s" % (flavour,test.name))
            self.stream.writeln(self.separator2)
            self.stream.writeln("%s" % err)

    def __repr__(self):
        return ("<%s run=%i failures=%i>" %
              ('xxxxxx', self.testsNo, len(self.failures)))
