# pylint: disable=W0201
import json
import os
import re
from time import sleep, time_ns
from datetime import datetime
import requests

from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from scripts.google_service import create_service, media_file_upload


class Helpers:
    config_file = os.path.abspath('../config.json')
    en_file = os.path.abspath('../../data/en.json')
    nl_file = os.path.abspath('../../data/nl.json')

    with open(config_file, 'r') as file:
        config = json.load(file)

    @staticmethod
    def wait_presence_by_id(driver, element, wait=20):
        return WebDriverWait(driver, wait).until(EC.presence_of_element_located((By.ID, element)))

    @staticmethod
    def wait_presence_by_xpath(driver, element, wait=20):
        return WebDriverWait(driver, wait).until(EC.presence_of_element_located((By.XPATH, element)))

    @staticmethod
    def wait_all_presence_by_xpath(driver, elements, wait=20):
        return WebDriverWait(driver, wait).until(EC.presence_of_all_elements_located((By.XPATH, elements)))

    @staticmethod
    def wait_visibility_by_xpath(driver, element, wait=20):
        return WebDriverWait(driver, wait).until(EC.visibility_of_element_located((By.XPATH, element)))

    @staticmethod
    def wait_invisibility_by_xpath(driver, element, wait=50):
        return WebDriverWait(driver, wait).until(EC.invisibility_of_element_located((By.XPATH, element)))

    @staticmethod
    def wait_clickable_by_id(driver, element, wait=20):
        return WebDriverWait(driver, wait).until(EC.element_to_be_clickable((By.ID, element)))

    @staticmethod
    def wait_clickable_by_xpath(driver, element, wait=20):
        return WebDriverWait(driver, wait).until(EC.element_to_be_clickable((By.XPATH, element)))

    @staticmethod
    def fluentwait_presence_by_xpath(driver, element):
        return WebDriverWait(driver, timeout=30, poll_frequency=1,
                             ignored_exceptions=[NoSuchElementException, StaleElementReferenceException]) \
            .until(EC.presence_of_element_located((By.XPATH, element)))

    @staticmethod
    def fluentwait_presence_by_id(driver, element):
        return WebDriverWait(driver, timeout=30, poll_frequency=1,
                             ignored_exceptions=[NoSuchElementException, StaleElementReferenceException]) \
            .until(EC.presence_of_element_located((By.ID, element)))

    @staticmethod
    def wait_presence_by_class_name(driver, element, wait=20):
        return WebDriverWait(driver, wait).until(EC.presence_of_element_located((By.CLASS_NAME, element)))

    @staticmethod
    def wait_url_contains(driver, url, wait=20):
        return WebDriverWait(driver, wait).until(EC.url_contains(url))

    @staticmethod
    def switch_window(driver, link):
        print(driver.current_url)

        # current_window = driver.current_window_handle
        link.click()

        # this loop will open any new window
        for handle in driver.window_handles:
            driver.switch_to.window(handle)

        print(driver.current_url)

    @staticmethod
    def press_enter(obj):
        return obj.send_keys(Keys.RETURN)

    @staticmethod
    def send_text(obj, txt):
        obj.clear()
        return obj.send_keys(txt)

    @staticmethod
    def slow_text_typing_clear_by_char(text_field, text_input, max_delete_key):
        sleep(3)
        for _ in range(max_delete_key):
            text_field.send_keys(Keys.BACK_SPACE)
        sleep(3)
        for character in text_input:
            text_field.send_keys(character)
            sleep(0.005)

    @staticmethod
    def slow_text_typing(text_field, text_input):
        sleep(3)
        text_field.clear()
        for character in text_input:
            text_field.send_keys(character)
            sleep(0.005)

    def en_text(self):
        with open(self.en_file, 'r') as file:
            strings_en = json.load(file)
        return strings_en

    def nl_text(self):
        with open(self.nl_file, 'r') as file:
            strings_nl = json.load(file)
        return strings_nl

    def dashboard_sub_url(self):
        return self.config["SUB_URL"]["DASHBOARD"]

    def library_url(self):
        return self.config["SUB_URL"]["LIBRARY"]

    def help_center_url(self):
        return self.config["SUB_URL"]["HELP_CENTER"]

    def webinars_url(self):
        return self.config["SUB_URL"]["WEBINARS"]

    def login_sub_url(self):
        return self.config["SUB_URL"]["LOGIN"]

    def get_page_login(self, driver, options):
        try:
            driver.get(self.config[options['environment']]['WEB_URL'])
        except Exception as error:
            print("Cannot open login page: \n", error)

    def get_freshdesk_url(self, driver):
        try:
            driver.get(self.config["FRESHDESK_URL"])
        except Exception as error:
            print("Cannot open freshdesk page: \n", error)

    def get_page_main(self, driver):
        url_page_main = self.config['SUB_URL']['DASHBOARD']
        if url_page_main not in driver.current_url:
            driver.get(url_page_main)

    def get_api_base_url(self, options):
        api_url = self.config[options['environment']]['WEB_URL'] + "/api/v1/"
        return api_url

    def get_client_search(self, options):
        env = self.config[options['environment']]
        browser = options['browser'].upper()
        return env[browser]["SEARCH_CLIENT_NAME"]

    def get_client2_search(self, options):
        env = self.config[options['environment']]
        browser = options['browser'].upper()
        return env[browser]["SEARCH_CLIENT2_NAME"]

    def get_client_search_second(self, options):
        env = self.config[options['environment']]
        browser = options['browser'].upper()
        return env[browser]["SEARCH_SECOND_CLIENT"]

    def get_therapist_edited_text(self, options):
        env = self.config[options['environment']]
        browser = options['browser'].upper()
        return env[browser]["THERAPIST_EDIT_TEXT"]

    def get_therapist2_name(self, options):
        env = self.config[options['environment']]
        browser = options['browser'].upper()
        return env[browser]["SEARCH_THERAPIST2_NAME"]

    @staticmethod
    def find_word(word, phrase):
        regex = '(?:' + word + ')'
        return re.search(regex, str(phrase))

    def get_static_therapist1(self, options):
        env = self.config[options['environment']]
        browser = options['browser'].upper()
        data = {
            'email': env[browser]['THERAPIST1_EMAIL'],
            'password': env['PASSWORD_EMAIL']
        }
        return data

    def get_static_client(self, options):
        env = self.config[options['environment']]
        browser = options['browser'].upper()
        data = {
            'client1': {
                'email': env[browser]['CLIENT1_EMAIL'],
                'password': env['PASSWORD_EMAIL']
            },
            'client2': {
                'email': env[browser]['CLIENT2_EMAIL'],
                'password': env['PASSWORD_EMAIL']
            }
        }
        return data

    def get_static_therapist2(self, options):
        env = self.config[options['environment']]
        browser = options['browser'].upper()
        data = {
            'therapist2': {
                'email': env[browser]['THERAPIST2_EMAIL'],
                'password': env['PASSWORD_EMAIL']
            }
        }
        return data

    # Get network id between client - therapist
    def get_static_network_id(self, options):
        return self.config[options['environment']]['NETWORK_ID_CLIENT']

    def get_client_auth_token(self, options):
        login_url = self.get_api_base_url(options) + 'auth/login/'
        login_data = self.get_static_client(options)
        response1 = requests.post(login_url, auth=(login_data['client1']['email'], login_data['client1']['password']))
        response2 = requests.post(login_url, auth=(login_data['client2']['email'], login_data['client2']['password']))
        token = {
            'client1': '{}'.format(response1.json()['token']),
            'client1_user': '{}'.format(response1.json()['user']['id']),
            'client2': '{}'.format(response2.json()['token']),
            'client2_user': '{}'.format(response2.json()['user']['id'])
        }
        return token

    def get_therapist_auth_token(self, options):
        login_url = self.get_api_base_url(options) + 'auth/login/'
        login_data1 = self.get_static_therapist1(options)
        login_data2 = self.get_static_therapist2(options)
        response_t1 = requests.post(login_url, auth=(login_data1['email'], login_data1['password']))
        response_t2 = requests.post(login_url,
                                    auth=(login_data2['therapist2']['email'], login_data2['therapist2']['password']))
        token = {
            'therapist1': '{}'.format(response_t1.json()['token']),
            'therapist1_user': '{}'.format(response_t1.json()['user']['id']),
            'therapist2': '{}'.format(response_t2.json()['token']),
            'therapist2_user': '{}'.format(response_t2.json()['user']['id'])
        }
        return token

    @staticmethod
    def create_auto_user():
        email = 'automation+' + str(time_ns()) + '@sense-os.nl'
        return {'email': email, 'password': 'Password$123'}

    @staticmethod
    def click_el_via_script(driver, element):
        driver.execute_script("arguments[0].click();", element)

    @staticmethod
    def scroll_down_to_element(driver, element):
        action = ActionChains(driver)
        return action.move_to_element(element).click().perform()

    @staticmethod
    def scroll_down_within_element(driver, element):
        # gets the element using css selector
        driver.execute_script("document.querySelector('" + element + "').scrollTop=500")

    @staticmethod
    def scroll_up_to_element(driver, element):
        coordinates = element.location_once_scrolled_into_view
        return driver.execute_script('window.scrollTo({}, {});'.format(coordinates['x'], coordinates['y']))

    @staticmethod
    def scroll_to_bottom(driver):
        return driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    @staticmethod
    def scroll_to_top(driver):
        return driver.execute_script("window.scrollTo(document.body.scrollHeight, 0);")

    @staticmethod
    def check_element_exist(element):
        try:
            element
        except NoSuchElementException:
            return False
        return True

    @staticmethod
    def remove_readonly(driver, element):
        return driver.execute_script("arguments[0].removeAttribute('readonly','readonly')", element)

    def close_any_toast(self, driver):
        try:
            while not None:
                try:
                    close = self.wait_clickable_by_xpath(driver, '//button[@type="button"][contains(text(),"×")]', 5)
                    close.click()
                except TimeoutException:
                    break
        except StaleElementReferenceException:
            pass

    @staticmethod
    def upload_to_google_drive(cache, request):
        config_file = os.path.abspath('../config.json')
        with open(config_file, 'r') as configuration:
            config = json.load(configuration)

        client_secret_file = config['DRIVE_API']['CLIENT_SECRET_FILE']
        api_name = config['DRIVE_API']['DRIVE_API_NAME']
        api_version = config['DRIVE_API']['DRIVE_API_VERSION']
        scopes = config['DRIVE_API']['DRIVE_SCOPES']
        browser = request.config.getoption("-B").lower()

        if browser == "chrome":
            parent_folder = config['FOLDER_SCREENSHOT_ID_CHROME']
        if browser == "firefox":
            parent_folder = config['FOLDER_SCREENSHOT_ID_FIREFOX']

        service = create_service(client_secret_file, api_name, api_version, scopes)

        file_name = cache.get("web-goalie/file-name", None)
        file_metadata = {
            'name': file_name,
            'parents': [parent_folder]
        }
        print(file_name)
        media = media_file_upload(os.path.abspath('../screenshots/{0}'.format(file_name)),
                                  mime_type='image/png')
        service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()

    # make a screenshot with a name of the test, date and time
    @staticmethod
    def take_screenshot(driver, request, cache):
        node_id = request.node.nodeid

        class Cd:
            """Context manager for changing the current working directory"""

            def __init__(self, new_path):
                self.new_path = os.path.expanduser(new_path)

            def __enter__(self):
                try:
                    self.saved_path = os.getcwd()
                    os.chdir(self.new_path)
                except OSError:
                    os.mkdir(self.new_path)
                    self.saved_path = os.getcwd()
                    os.chdir(self.new_path)

            def __exit__(self, etype, value, traceback):
                os.chdir(self.saved_path)

        with Cd("../screenshots"):
            sleep(1)
            file_name = f'{node_id.split("::")[2]}_{datetime.today().strftime("%Y-%m-%d_%H:%M")}.png'.replace("::",
                                                                                                              "__")
            driver.save_screenshot(file_name)
            cache.set("web-goalie/file-name", file_name)
            sleep(5)
            if request.config.getoption("-U").lower() == 'y':
                Helpers.upload_to_google_drive(cache, request)
