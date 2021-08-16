from qaseio.pytest import qase


class TestAuthLogin:

    @qase.id(1)
    def test_login_with_valid_data(self, page, ):
        # Login to portal
        page.goto('https://beta.niceday.app/')
        page.fill("//input[@id='email']", "azkia+therapist+beta+4@sense-os.nl")
        page.fill("//input[@id='password']", "Test@12345")
        page.click('text=login')

        # Assertion
        assert page.inner_text('h1') == 'Hi, Azkia Therapist'

        # Logout
        page.click("text=Azkia Therapist Stand Up")
        page.click("text=Log out")

        assert page.inner_text('h5') == 'Sign in'

    @qase.id(2)
    def test_login_blank_email_invalid_password(self, page):
        # Go to login page
        page.goto('https://beta.niceday.app/')
        page.fill("//input[@id='email']", "azkia+therapist+beta+4@sense-os.nl")
        page.fill("//input[@id='password']", "Test@1234578")
        page.click('text=login')

        # Assertion
        assert page.inner_text() == 'Invalid username or password'

    @qase.id(3)
    def test_login_blank_email_valid_password(self, page):
        # Go to login page
        # Go to login page
        page.goto('https://beta.niceday.app/')
        page.fill("//input[@id='email']", "azkia+therapist+beta+4@uvuvu-os.nl")
        page.fill("//input[@id='password']", "Test@12345")
        page.click('text=login')

        # Assertion
        assert page.inner_text('p') == 'Invalid username or password'
