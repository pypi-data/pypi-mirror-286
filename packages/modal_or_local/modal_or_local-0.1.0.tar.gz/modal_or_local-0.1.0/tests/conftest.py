import pytest
import inspect
import subprocess


def pytest_addoption(parser):
    parser.addoption("--myoption", action="store_true", help="Enable my custom option")


def pytest_configure(config):
    if config.option.myoption:
        print("Custom option '--myoption' is enabled!")


def pytest_collection_modifyitems(config, items):
    """
    Modify each of the gathered tests to add the modal_runner marker as needed
    """
    for item in items:
        if _is_modal_test(item):
            item.add_marker(pytest.mark.modal_run)


def _is_modal_test(item):
    """
    Checks if the given test item is a modal test based on the decorator.
    """
    try:
        test_func = item.function
        print(f"{test_func=}")
        source_lines, _ = inspect.getsourcelines(test_func)
        for line in source_lines:
            print(f"{__file__} source {line=}")
            if "@app.function" in line:
                return True
    except (AttributeError, IOError):
        pass
    return False


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item):
    if "modal_run" in item.keywords:
        subprocess.check_call(["modal", "run", "test_modal_or_local.py"])
