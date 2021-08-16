import json
import os
import tempfile
import requests


class SlackReport:

    def post_reports_to_slack(self, session):

        with open(os.path.abspath('../config.json'), 'r') as file:
            config = json.load(file)

        browser_option = session.config.getoption("-B").lower()
        env_option = session.config.getoption("-E")
        headless_option = session.config.getoption("-H").lower()
        portal_version = session.config.cache.get("web-goalie/version", 'x.x')
        be_version = self.get_backend_version(config[env_option]["WEB_URL"] + "/api/v1/")
        slack_channel = config[env_option][browser_option.upper()]["SLACK_HOOK"]

        with open(os.path.abspath('../test/pytest_report.log'), "r") as in_file:
            failed_report = ""
            number_line = 1
            number_test = 0
            number_test_pass = 0
            number_test_fail = 0
            title = ""
            for line in in_file:
                if number_line > 6:
                    if number_line == 8:
                        title = line.split("::")[1]

                    if 'PASSED' in line:
                        number_test += 1
                        number_test_pass += 1
                    elif 'FAILED' in line:
                        number_test += 1
                        number_test_fail += 1
                        failed_report = failed_report + '\n' + line

                number_line += 1

        if number_test == 0:
            return

        if number_test_fail > (number_test/2):
            failed_report = 'Info: too many failed test, please check the log file,'

        icon_status = ':white_check_mark:'
        icon_report = ':chrome:'
        bar_color = "#36a64f"

        if number_test_fail > 1:
            icon_status = ':x:'
            bar_color = "#ff0000"
        if browser_option == 'firefox':
            icon_report = ':firefox:'
        if browser_option == 'safari':
            icon_report = ':safari:'

        final_output = icon_report + ' ' + title + ' Passed:  ' + str(number_test_pass) + ' / ' + str(number_test)
        final_output += ' -- ' + browser_option.capitalize() + '/' + portal_version + ' /BE: ' + be_version + ' ' + icon_status

        data = {
            "text": final_output,
            "attachments": [
                {
                    "color": bar_color,
                    "text": failed_report,
                    "mrkdwn_in": ["text"]
                }
            ]
        }

        json_params_encoded = json.dumps(data)
        slack_response = requests.post(url=slack_channel, data=json_params_encoded,
                                       headers={"Content-type": "application/json"})

        if slack_response.text == 'ok':
            print("\nSuccessfully posted pytest report on Slack channel")
        else:
            print("\nSomething went wrong. Unable to post pytest report on Slack channel. Slack Response:'" +
                  str(slack_response))

        headless_option = "No"
        # Set allure environment properties
        if headless_option == "y":
            headless_option = "Yes"

        env_file = '../allure/allure-results/environment.properties'
        self.set_properties(env_file, "Portal.Version", portal_version + "\n")
        self.set_properties(env_file, "Backend.Version", be_version + "\n")
        self.set_properties(env_file, "Browser", browser_option.capitalize() + "\n")
        self.set_properties(env_file, "Headless", headless_option)

    @staticmethod
    def set_properties(filename, key, value):
        with open(filename, 'r') as f_in, tempfile.NamedTemporaryFile(
                'w', dir=os.path.dirname(filename), delete=False) as f_out:
            for line in f_in.readlines():
                if line.startswith(key):
                    line = '='.join((line.split('=')[0], ' {}'.format(value)))
                f_out.write(line)

        # remove old version
        os.unlink(filename)
        # rename new version
        os.rename(f_out.name, filename)

    @staticmethod
    def get_backend_version(url):
        return requests.get(url).headers['X-API-Version']
