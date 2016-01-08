import sys
import traceback
import datetime
from StringIO import StringIO

__stest = True
result_str  ="""
Test Build          %(projectName)s
Start Time          %(startTime)s
Stop Time           %(stopTime)s
Duration            %(timeTaken)s seconds
Statistics
    All=%(total)d Passed=%(passed)d Failed=%(failed)d Aborted=%(aborted)d
"""
class TestResult(object):
    separator1 = '=' * 70
    separator2 = '-' * 70

    def __init__(self,stream=None):
        self.stream = stream
        self.log = StringIO()
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
        self.writeStream(regulateInfo(str(test), 'start to run...'))
        self.stream.flush()

    def stopTest(self, test):
        """Called when the given test has been run"""
        self.writeStream(regulateInfo(str(test), 'stop running.'))
        self.stream.flush()

    def addSuccess(self, test):
        "Called when a test has completed successfully"
        self.testsNo += 1
        self.writeStream(regulateInfo(str(test), 'test success.'))
        self.successes.append((test, ''))
        self.results.append([str(test), 'Passed'])

    def addFailure(self, test, err):
        self.testsNo += 1
        self.writeStream(regulateInfo(str(test), 'test failed:'))
        self.writeStream(self._exc_info_to_string(err, test), False)
        self.failures.append((test, self._exc_info_to_string(err, test)))
        self.results.append([str(test), 'Failed', self._exc_info_to_string(err, test)])

    def addError(self, test, err):
        self.testsNo += 1
        self.writeStream(regulateInfo(str(test), 'test aborted:'))
        self.writeStream(self._exc_info_to_string(err, test), False)
        self.failures.append((test, self._exc_info_to_string(err, test)))
        self.results.append([str(test), 'Aborted', self._exc_info_to_string(err, test)])

    def writeStream(self, stream, line=True):
        self.stream.write(stream)
        self.log.write(stream)
        if line:
            self.stream.write('\n')
            self.log.write('\n')

    def _exc_info_to_string(self, err, test):
        """Converts a sys.exc_info()-style tuple of values into a string."""
        if isinstance(err, tuple):
            exctype, value, tb = err
            # Skip test runner traceback levels
            while tb and self._is_relevant_tb_level(tb):
                tb = tb.tb_next
            if exctype is test.failureException:
                # Skip assert*() traceback levels
                length = self._count_relevant_tb_levels(tb)
                msgLines = traceback.format_exception(exctype, value, tb, length)
            else:
                msgLines = traceback.format_exception(exctype, value, tb)
            return ''.join(msgLines)
        else:
            return str(err)

    def _is_relevant_tb_level(self, tb):
        return '__stest' in tb.tb_frame.f_globals

    def _count_relevant_tb_levels(self, tb):
        length = 0
        while tb and not self._is_relevant_tb_level(tb):
            length += 1
            tb = tb.tb_next
        return length

    def wasSuccessful(self):
        "Tells whether or not this result was a success"
        return len(self.failures) == 0

    def printResult(self):
        result_data = {'passed': len(self.successes), 'failed': len(self.failures),
            'aborted': len(self.errors), 'projectName': self.projectName,
            'startTime': self.startTime,'stopTime': self.stopTime,
            'timeTaken':self.timeTaken,'total': self.testsNo}
        self.writeStream(result_str % result_data)

def getCurrentTimeStr():
    now = datetime.datetime.now()
    return datetime.datetime.strftime(now, '%Y.%m.%d %H:%M:%S.%f')


def regulateInfo(caseName, info):
    return '[%s][%s]: %s' % (getCurrentTimeStr(), caseName, info)
