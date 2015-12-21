import os
import sys
import json

from functools import cmp_to_key as _CmpToKey
from fnmatch import fnmatch

import case

sys.path.append('')

class TestLoader(object):
    suiteClass = case.TestSuite
    testMethodPrefix = 'tc_'
    sortTestMethodsUsing = cmp
    driverHomePath = '/Users/wangming/workspace/etest/driverHomePath'

    def listDrivers(self):
        import StringIO
        driver_list = StringIO.StringIO()
        files = os.listdir(self.driverHomePath)
        for f in files:
            if '.' not in f:
                driver_list.write('%s   ' % f)
        driver_list.seek(0)
        return driver_list.read()

    def loadDriverFromName(self,name):
        driverPath = os.path.join(self.driverHomePath, name)
        os.chdir(driverPath)
        setUpFunc = getattr(__import__('setUp'),'setUp')
        tearDownFunc = getattr(__import__('tearDown'),'tearDown')
        execModule = __import__('exec')
        testFnNames = self.getTestFuncNames(execModule)
        return case.TestDriver(name, execModule, testFnNames,setUpFunc=setUpFunc, tearDownFunc=tearDownFunc)

    def loadTestsFromFile(self, f, prefix=None):
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
        return self.suiteClass([test])

    def loadTestsFromDir(self, dir):
        print 'load tests from dir:%s' % dir
        if not self._math_path(os.path.basename(dir), 'ts_*'):
            print 'error'
            return
        prefix = os.path.basename(dir)
        tests = list(self._find_tests(dir,prefix=prefix))
        return self.suiteClass(tests)

    def loadTestsFromPlan(self, plan):
        plan_json = json.load(file(plan))
        case_list = plan_json["Case List"]
        case_list = case_list.split(",")
        tests = []
        cases = []
        for c in case_list:
            cases.append(os.path.abspath(c))
        for c in cases:
            if os.path.isdir(c):
                tests.append(self.loadTestsFromDir(c))
            elif os.path.isfile(c):
                tests.append(self.loadTestsFromFile(c))
        return plan_json, self.suiteClass(tests)

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
