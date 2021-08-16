import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from scripts.slack_report import SlackReport
from scripts.helpers import Helpers


@pytest.fixture
def options(request):
    env_option = request.config.getoption("-E")
    return {'environment': env_option}


@pytest.fixture(scope="session", autouse=True)
def driver(request):
    web_driver = webdriver.Chrome()
    web_driver.set_window_size(1920, 1080)
    web_driver.set_window_position(0, 0)
    session = request.node
    for item in session.items:
        cls = item.getparent(pytest.Class)
        setattr(cls.obj, "driver", web_driver)
    yield web_driver
    web_driver.close()


def pytest_addoption(parser):
    # add parser options
    parser.addoption("-I", "--slack_integration_flag", default="N",
                     help="Post the test report on slack channel: Y or N")

    parser.addoption("-E", "--environment", default="ALPHA_ENV",
                     help="option: [ALPHA/BETA/PROD]_ENV")

    parser.addoption("-H", "--headless_browser_flag", default="N",
                     help="Running test without GUI: Y or N")

    parser.addoption("-U", "--upload", dest="capture_upload", default="N",
                     help="Capture fail step then upload to google drive")


# set up a hook to be able to check if a test has failed
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()

    # set a report attribute for each phase of a call, which can
    # be "setup", "call", "teardown"

    setattr(item, "rep_" + rep.when, rep)


# check if a test has failed
@pytest.fixture(scope="function", autouse=True)
def test_failed_check(request, driver, cache):
    yield
    # request.node is an "item" because we use the default
    # "function" scope
    if request.node.rep_setup.failed:
        print("setting up a test failed!", request.node.nodeid)
    elif request.node.rep_setup.passed:
        if request.node.rep_call.failed:
            Helpers.take_screenshot(driver, request, cache)
            # print("executing test failed", request.node.nodeid)


def pytest_sessionfinish(session):
    # executes after whole test run finishes
    if session.config.getoption("-I").lower() == 'y':
        SlackReport().post_reports_to_slack(session)
