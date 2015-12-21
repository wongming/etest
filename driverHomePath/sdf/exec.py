def tc_hello(tc):
    print 'tc_hello'
    print tc.name
    assert False, 'hello'

def tc_bye(tc):
    print 'tc_bye'
    print tc.age
    assert True, 'bye'
