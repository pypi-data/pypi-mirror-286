import pytest

# https://docs.pytest.org/en/7.1.x/reference/reference.html#hook-reference

def pytest_runtest_setup(item):
    print("pytest_runtest_setup")
    print(item)
    print("hi")

# pytest_generate_tests

# pytest_collection_modifyitems(session, config, items)
# session.items

# pytest_runtestloop(session)

# pytest_pyfunc_call(pyfuncitem)
