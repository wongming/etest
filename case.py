class TestDriver(object):
    def __init__(self,name, execFunc, setUpFunc=None, tearDownFunc=None):
        self._name = name
        self._setUpFunc = setUpFunc
        self._tearDownFunc = tearDownFunc
        self._execFunc = execFunc
    def setUp(self):
        print 'Driver:%s set up fixture...'
        self._setUpFunc(self)

    def tearDown(self):
        print 'Driver:%s tear down fixture...'
        self._tearDownFunc(self)

    def runCase(self, tm):
        testMethod = getattr(self._execFunc,tm)
        testMethod(self)

class TestSuite(object):
    def __init__(self, tests, drivers):
        self._tests = tests
        self._drivers = drivers
        self._previousDriver = None
        self._currentDriver = None

    def __iter__(self):
        return iter(self._tests)

    def __call__(self, *args, **kwds):
        return self.run(*args, **kwds)

    def run(self, result):
        for test in self:
            self._tearDownPreviousFixture(test, result)
            self._setUpFixture(test, result)
            result._previousDriver = test.driver
            #run case
            self._runCase(test,result)
        return result
    def _runCase(self, test, result):
        driver = self._drivers[test.driver]
        driver.runCase(test.testFn)

    def _handleFixtrue(self, test, result):
        previousDriver = result._previousDriver
        if not previousDriver:
            self._currentDriver = self._drivers[test.driver]
            self._setUpFixture(result)
        elif (previousDriver!=test.driver):
            self._tearDownPreviousFixture(result)
            self._currentDriver = self._drivers[test.driver]
            self._setUpFixture(result)
        result._previousDriver = self._currentDriver

    def _setUpFixture(self, result):
        self._currentDriver.setUp()

    def _tearDownPreviousFixture(self, result):
        self._currentDriver.tearDown()

    def countTestCases(self):
        cases = 0
        for test in self:
            cases += test.countTestCases()
        return cases

    def addTest(self, test):
        self._tests.append(test)

    def addTests(self, tests):
        for test in tests:
            self.addTest(test)

    def addDriver(self, driver):
        self.drivers.update({driver.name:driver})

class TestCase(object):
    def __init__(self,name,driver,testFn):
        self.name = name
        self.driver =driver
        self.testFn = testFn

    def run(self, result):
        print 'run case...'

    def __call__(self, *args, **kwds):
        return self.run(*args, **kwds)
