# pylint: disable=missing-function-docstring
# pylint: disable=C0114
def test_example_login(page):
    page.goto("https://beta.niceday.app/")
    page.fill("//input[@id='email']", "email")
    page.fill("//input[@id='password']", "password")
    page.click("//span[contains(text(),'Login')]")
