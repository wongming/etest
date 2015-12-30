class TestSuite(object):
    def __init__(self, setup=None, teardown=None):
        self.setup = setup
        self.teardown = teardown
        self.cases = []
        self.tc = Case()

    def setUp(self):
        print 'setUp...'
        self.setup(self.tc)

    def tearDown(self):
        print 'tearDown...'
        self.teardown(self.tc)

    def run(self):
        self.setUp()
        print 'runTests...'
        for c in self.cases:
            c.run(self.tc)
        self.tearDown()

class TestCase(object):
    def __init__(self):
        pass
    def run(self,tc):
        print 'run case...'
        self.runTests(tc)
