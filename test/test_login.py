# pylint: disable=invalid-name
# pylint: disable=C0114
# pylint: disable=C0115
# pylint: disable=C0116
# pylint: disable=C0303

import os
import json
from qaseio.pytest import qase

class TestLogin():
    config_file = os.path.abspath('../obj_screen/auth.json')
    with open(config_file, 'r') as configuration:
        obj_auth = json.load(configuration)

    @qase.id(1)
    def test_example_login(self, page):
        page.goto(self.obj_auth['web_link'])
        page.fill(self.obj_auth['email_field'], "test")
        page.fill(self.obj_auth['password_field'], "test")
        page.click(self.obj_auth['login_btn'])
    
    def test_login(self, page):
        page.goto(self.obj_auth['web_link'])
        page.fill(self.obj_auth['email_field'], "test")
        page.fill(self.obj_auth['password_field'], "test")
        page.click(self.obj_auth['login_btn'])
