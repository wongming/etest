import sys

from stest import result

__stest = True

class TestDriver(object):
    def __init__(self, name, execModule, testMethods, setUpFunc=None, tearDownFunc=None):
        self.name = name
        self.execModule = execModule
        self.testMethods = testMethods
        self.setUpFunc = setUpFunc
        self.tearDownFunc = tearDownFunc

class TestSuite(object):
    def __init__(self, tests, projectName=None):
        self._tests = tests
        self._previousDriver = None
        self._currentDriver = None
        if projectName:
            self.projectName = projectName

    def __iter__(self):
        return iter(self._tests)

    def __call__(self, *args, **kwds):
        return self.run(*args, **kwds)

    def run(self, result):
        for test in self:
            test.run(result)
        return result

    def countTestCases(self):
        cases = 0
        for test in self:
            cases += test.countTestCases()
        return cases

class TestCase(object):
    def __init__(self, name, driver, error=False, errMsg=None):
        self._name = name
        if driver:
            self.driver = driver.name
            self.testMethods = driver.testMethods
            self._execModule = driver.execModule
            self._setUpFunc = driver.setUpFunc
            self._tearDownFunc = driver.tearDownFunc
        else:
            self.driver = None
        self.currentTestMethod = None
        self.failureException = AssertionError
        self.error = error
        self.errMsg = errMsg

    def setUp(self):
        self._setUpFunc(self)

    def tearDown(self):
        self._tearDownFunc(self)

    def __str__(self):
        if self.currentTestMethod:
            return '%s#%s' % (self._name, self.currentTestMethod)
        else:
            return '%s' % (self._name)

    def _addErrorList(self, result, error):
        for testMethod in self.testMethods:
                self.currentTestMethod = testMethod
                result.addError(self, error)

    def run(self, result):
        result.startTest(self)
        try:
            if self.error:
                result.addError(self, self.errMsg)
            else:
                try:
                    self.setUp()
                except KeyboardInterrupt:
                    raise
                except:
                    result.writeStream(sys.exc_info())
                    self._addErrorList(self, result, 'Driver:%s of %s set up error.' % (self.driver, self._name) )
                else:
                    for testMethod in self.testMethods:
                        self.currentTestMethod = testMethod
                        result.startTest(self)
                        testFn = getattr(self._execModule, testMethod)
                        try:
                            testFn(self)
                        except KeyboardInterrupt:
                            raise
                        except AssertionError:
                            result.addFailure(self, sys.exc_info())
                        except:
                            result.addError(self, sys.exc_info())
                        else:
                            result.addSuccess(self)
                        finally:
                            result.stopTest(self)
                    try:
                        self.tearDown()
                    except KeyboardInterrupt:
                        raise
                    except:
                        result.writeStream(sys.exc_info())
                        result.writeStream('Driver:%s of %s tear down error.' % (self.driver, self._name))
        finally:
            self.currentTestMethod =None
            result.stopTest(self)
