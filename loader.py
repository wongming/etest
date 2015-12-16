import os
import sys
import json

from functools import cmp_to_key as _CmpToKey

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
        execFunc = __import__('exec')
        return case.TestDriver(name, execFunc, setUpFunc=setUpFunc, tearDownFunc=tearDownFunc)

    def loadTestsFromNamesOfADriver(self, names, dir):
        print 'load tests from %s of %s' % (names, dir)
        dir = os.path.normpath(dir)
        driverName = dir.split('/')[-1].replace('ts_','')
        os.chdir(os.path.join(dir,'conf'))
        exex =  __import__('exec')
        testFuncNames = self.getTestFuncNames(exex)
        if not testFuncNames and hasattr(exex, 'runTest'):
            testFuncNames = ['runTest']
        for name in names:
            for testFuncName in testFuncNames:
                if testFuncName =='runTest':
                    caseName = driverName+'#'+name.replace('tc_','')
                else:
                    caseName = driverName+'.'+testFuncName.replace('tc_','')+'#'+name.replace('tc_',+'')
                testCase = case.TestCase()
                testCase.driverName = driverName
        return self.suiteClass()


    def loadTestsFromFile(self, name, testFnNames=None):
        f = file(name)
        f = json.load(f)
        keys = f.keys()
        if 'driver' not in keys:
            print 'error'
        driverName = f['driver']
        driver = self.loadDriverFromName(driverName)
        if not testFnNames:
            testFnNames = self.getTestFuncNames(driverName)
        tests = []
        for testFnName in testFnNames:
            testName = name+'#'+testFnName
            test = case.TestCase(testName, driverName, testFnName)
            tests.append(test)
        print tests
        return self.suiteClass(tests,{driverName:driver})

    def loadTestsFromDir(self, dir):
        print 'load tests from dir:%s' % dir

        return

    def loadTestsFromPlan(self, plan):

        return

    def getTestFuncNames(self, driver):
        os.chdir(os.path.join(self.driverHomePath, driver))
        module = __import__('exec')
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
    suite = defaultTestLoader.loadTestsFromFile('tc_d2')
    import result

    suite.run(result.TestResult())
