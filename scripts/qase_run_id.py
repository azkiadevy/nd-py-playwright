import sys
from configparser import ConfigParser
from datetime import datetime

import json
import requests


CONFIG = ConfigParser()

CONFIGURATION = '../pytest.ini'
CONFIG.read(CONFIGURATION)

TEST_RUN_URL = 'https://api.qase.io/v1/run/ND'
TEST_PLAN_URL = 'https://api.qase.io/v1/plan/ND'
PLAN_ID = '91'
QASE_TOKEN = '3298b72cd24a234f5607ec21e4bd6415cd65cf33'


# get list of the test_case_id's from selected 'PLAN_ID'
QASE_RESPONSE = requests.get(url=TEST_PLAN_URL + '/' + str(PLAN_ID), headers={"Token": QASE_TOKEN, "Content-type": "application/json"})

RESPONSE_DATA = QASE_RESPONSE.json()
CASES = RESPONSE_DATA['result']['cases']

CASE_ID = []
for x in CASES:
    CASE_ID.append(x['case_id'])

# create test_run with the list of the test_case_id
DATA = {"title": "test ", "cases": CASE_ID}
JSON_PARAMS_ENCODED = json.dumps(DATA)
QASE_RESPONSE = requests.post(url=TEST_RUN_URL, headers={"Token": QASE_TOKEN, "Content-type": "application/json"}, data=JSON_PARAMS_ENCODED)

RESPONSE_DATA = QASE_RESPONSE.json()
RUN_ID = str(RESPONSE_DATA['result']['id'])

if RESPONSE_DATA['status']:
    print("Successfully create test run ID : " +
          RUN_ID)
else:
    print("Something went wrong" +
          str(RESPONSE_DATA))


# replace 'test run_id' in config with the new data
CONFIG.set('pytest', 'qs_testrun_id', RUN_ID)
with open(CONFIGURATION, 'w') as new_id:
    CONFIG.write(new_id)
