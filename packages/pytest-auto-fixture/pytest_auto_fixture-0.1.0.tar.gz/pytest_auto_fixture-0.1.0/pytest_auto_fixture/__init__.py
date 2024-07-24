__author__ = 'dpepper'
__version__ = '0.1.0'


def pytest_runtest_call(item):
    req = item._request
    manager = item.session._fixturemanager
    fixtures = item.session._fixturemanager._arg2fixturedefs.keys()

    # find missing references
    refs = item.obj.__code__.co_names & fixtures

    for ref in refs:
        # if a different reference is already in scope, skip
        global_ref = item.function.__globals__.get(ref)
        if global_ref and not hasattr(global_ref, '_pytestfixturefunction'):
            continue

        fixture = manager.getfixturedefs(ref, item)[0]
        res = item.ihook.pytest_fixture_setup(fixturedef=fixture, request=req)

        item.function.__globals__[ref] = res
