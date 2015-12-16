class TestRunner(object):
    def __init__(self, stream=sys.stdout,resultclass=None):
        if resultclass is not None:
            self.resultclass = resultclass
        else:
            self.resultclass = TextTestResult

    def _makeResult(self):
        return self.resultclass(stream=self.stream)

    def run(self, test):
        result = self._makeResult()
        startTime = time.time()
        startTestRun = getattr(result, 'startTestRun', None)
        if startTestRun is not None:
            startTestRun()
        try:
            test(result)
        finally:
            stopTestRun = getattr(result, 'stopTestRun', None)
            if stopTestRun is not None:
                stopTestRun()
        stopTime = time.time()
        timeTaken = stopTime - startTime
        result.printResults()
        return result

defaultTestRunner = TestRunner()
