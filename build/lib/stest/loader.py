import os
import sys
import json
import ConfigParser
from functools import cmp_to_key as _CmpToKey
from fnmatch import fnmatch
from stest import case
sys.path.append('')

__stest = True

class TestLoader(object):

    def __init__(self):
        self.suiteClass = case.TestSuite
        self.testMethodPrefix = 'tc_'
        self.sortTestMethodsUsing = cmp
        conf = ConfigParser.ConfigParser()
        self.driverPath = os.path.expanduser('~/.stest/driver')
        if os.path.exists(os.path.expanduser('~/.stest/stest.conf')):
            conf.read(os.path.expanduser('~/.stest/stest.conf'))
            self.driverPath = os.path.expanduser(conf.get('base','DriverPath'))

    def listDrivers(self):
        import StringIO
        driver_list = StringIO.StringIO()
        files = os.listdir(self.driverPath)
        for f in files:
            if '.' not in f:
                driver_list.write('%s   ' % f)
        driver_list.seek(0)
        return driver_list.read()

    def loadDriverFromName(self,name):
        driverPath = os.path.join(self.driverPath, name)
        os.chdir(driverPath)
        setUpFunc = getattr(__import__('setUp'),'setUp')
        tearDownFunc = getattr(__import__('tearDown'),'tearDown')
        execModule = __import__('exec')
        testFnNames = self.getTestFuncNames(execModule)
        return case.TestDriver(name, execModule, testFnNames,setUpFunc=setUpFunc, tearDownFunc=tearDownFunc)

    def loadTestsFromFile(self, f, prefix=None, projectName=None):
        caseName = os.path.basename(f)
        if prefix:
            caseName = prefix +'.'+caseName
        f = file(f)
        f = json.load(f)
        keys = f.keys()
        if 'driver' not in keys:
            print 'error'
        driverName = f['driver']
        driver = self.loadDriverFromName(driverName)
        test = case.TestCase(caseName, driver)
        return self.suiteClass([test], projectName=projectName)

    def loadTestsFromDir(self, dir, projectName=None):
        #print 'load tests from dir:%s' % dir
        if not self._math_path(os.path.basename(dir), 'ts_*'):
            print 'error'
            return
        prefix = os.path.basename(dir)
        tests = list(self._find_tests(dir, prefix=prefix))
        return self.suiteClass(tests, projectName=projectName)

    def loadTestsFromPlan(self, plan):
        plan_json = json.load(file(plan))
        base_dir = os.path.dirname(plan)
        case_list = plan_json["Case List"]
        case_list = case_list.split(",")
        tests = []
        cases = []
        for caseName in case_list:
            caseFile = os.path.join(base_dir, caseName)
            if os.path.isdir(caseFile):
                tests.append(self.loadTestsFromDir(caseFile))
            elif os.path.isfile(caseFile):
                tests.append(self.loadTestsFromFile(caseFile))
            else:
                tests.append(self.make_failed_test(caseName, 'No such file or directory: %s' % caseFile))
        return plan_json, self.suiteClass(tests, projectName=plan_json["Plan Name"])

    def make_failed_test(self, name, err):
        test = case.TestCase(name, None, error=True, errMsg=err)
        return self.suiteClass([test])

    def _find_tests(self, start_dir, prefix=None):
        start_dir = os.path.abspath(start_dir)
        paths = os.listdir(start_dir)
        for path in paths:
            full_path = os.path.join(start_dir, path)
            if os.path.isfile(full_path):
                if not self._math_path(path, 'tc_*'):
                    continue
                yield self.loadTestsFromFile(full_path, prefix=prefix)
            elif os.path.isdir(full_path):
                if not self._math_path(path, 'ts_*'):
                    continue
                if prefix:
                    prefix = prefix+'.'+path
                else:
                    prefix = path
                for test in self._find_tests(full_path, prefix=prefix):
                    yield test


    def _math_path(self, path, pattern):
        return fnmatch(path, pattern)

    def getTestFuncNames(self, module):
        def isTestMethod(attrname, module=module,
                         prefix=self.testMethodPrefix):
            return attrname.startswith(prefix) and hasattr(getattr(module, attrname), '__call__')
        testFnNames = filter(isTestMethod, dir(module))
        if not testFnNames and ('runTest' in dir(module)):
            testFnNames = ['runTest']
        if self.sortTestMethodsUsing:
            testFnNames.sort(key=_CmpToKey(self.sortTestMethodsUsing))
        return testFnNames

defaultTestLoader = TestLoader()

if __name__=="__main__":
    #suite = defaultTestLoader.loadTestsFromFile('tc_d2')
    suite = defaultTestLoader.loadTestsFromDir('ts_lay1')
    import result
    suite.run(result.TestResult())
