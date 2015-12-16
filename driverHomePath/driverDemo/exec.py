def runTest(tc):
    i = tc.param['in']
    o = tc.param['expect']
    assert i==o,'in and expect not equal'

def tc_hello(tc):
    print 'tc_hello'
    print tc.name
    assert True, 'hello'

def tc_bye(tc):
    print 'tc_bye'
    print tc.age
    assert True, 'bye'
