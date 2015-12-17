import os
import sys
import json

from functools import cmp_to_key as _CmpToKey
from fnmatch import fnmatch

import case

sys.path.append('')

"""
    Examples:
        stest -rt ts_xxx           - run tests from a driver
        stest -rt ts_xxx#tm_xxx    - run tests from a test method
        stest -rt ts_xxx           - run tests from a dir
        stest -rp xxx.plan.json    - run plan
"""
class TestLoader(object):
    suiteClass = case.TestSuite
    testMethodPrefix = 'tc_'
    sortTestMethodsUsing = cmp
    driverHomePath = '/Users/wangming/workspace/etest/driverHomePath'

    def loadDriverFromName(self,name):
        driverPath = os.path.join(self.driverHomePath, name)
        os.chdir(driverPath)
        setUpFunc = getattr(__import__('setUp'),'setUp')
        tearDownFunc = getattr(__import__('tearDown'),'tearDown')
        execModule = __import__('exec')
        testFnNames = self.getTestFuncNames(execModule)
        return case.TestDriver(name, execModule, testFnNames,setUpFunc=setUpFunc, tearDownFunc=tearDownFunc)

    def loadTestsFromFile(self, f):
        caseName = os.path.basename(f)
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
        tests = list(self._find_tests(dir))
        return self.suiteClass(tests)

    def loadTestsFromPlan(self, plan):

        return
    def _find_tests(self,start_dir):
        start_dir = os.path.abspath(start_dir)
        start_dir = os.path.abspath(start_dir)
        paths = os.listdir(start_dir)
        for path in paths:
            full_path = os.path.join(start_dir, path)
            if os.path.isfile(full_path):
                if not self._math_path(path, 'tc_*'):
                    continue
                yield self.loadTestsFromFile(full_path)
            elif os.path.isdir(full_path):
                if not self._math_path(path, 'ts_*'):
                    continue
                for test in self._find_tests(full_path):
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
    suite = defaultTestLoader.loadTestsFromDir('ts_testts')
    import result
    suite.run(result.TestResult())
