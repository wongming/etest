def runTest(tc):
    i = tc.param['in']
    o = tc.param['expect']
    assert i==o,'in and expect not equal'

def tc_hello(tc):
    assert True, 'hello'

def tc_bye(tc):
    assert True, 'bye'
