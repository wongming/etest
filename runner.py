import sys
import time

import result
class TestRunner(object):
    def __init__(self, stream=sys.stderr,resultclass=None):
        if resultclass is not None:
            self.resultclass = resultclass
        else:
            self.resultclass = result.TestResult
        self.stream = stream

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
        result.startTime = startTime
        result.stopTime = stopTime
        result.timeTaken = timeTaken
        result.printResults()
        return result

defaultTestRunner = TestRunner()
