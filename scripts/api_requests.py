from datetime import datetime, timedelta
import requests
from scripts.helpers import Helpers


class APIRequests:

    helpers = Helpers()

    def create_client_diary_entry(self, options):
        current_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        create_diary_url = self.helpers.get_api_base_url(options) + 'sensor/?user_id=me'
        head = {'Authorization': 'token {}'.format(self.helpers.get_client_auth_token(options)['client1'])}
        create_diary_body = [{
            "sensor_name": "diary_entry",
            "source_name": "goalie_2",
            "start_time": "{}".format(current_time),
            "end_time": "{}".format(current_time),
            "version": 3,
            "value": {
                "title": "Diary Entry from UI automation test client",
                "description": "This data come from python requests",
                "happenedAt": "{}".format(current_time),
                "activityType": "EXPOSURE_ACTIVITY"
            }
        }]
        try:
            requests.post(create_diary_url, headers=head, json=create_diary_body)
        except requests.exceptions.HTTPError as error:
            print(error)
            print("Failed to create plan event.")

    def create_client_plan_event(self, options):
        plan_time = (datetime.utcnow() + timedelta(hours=2)).strftime('%Y-%m-%dT%H:%M:%SZ')
        create_event_url = self.helpers.get_api_base_url(options) + 'sensor/?user_id=me'
        head = {'Authorization': 'token {}'.format(self.helpers.get_client_auth_token(options)['client1'])}
        create_event_body = [{
            "sensor_name": "planned_event_entry",
            "source_name": "goalie_2",
            "start_time": "{}".format(plan_time),
            "end_time": "{}".format(plan_time),
            "version": 2,
            "value": {
                "title": "Plan event from UI automation test client",
                "description": "This data come from python requests",
                "shouldSendNotification": False,
                "plannedFor": "{}".format(plan_time),
                "status": "INCOMPLETED",
                "activityType": "FUN_ACTIVITY"
            }
        }]
        try:
            requests.post(create_event_url, headers=head, json=create_event_body)
        except requests.exceptions.HTTPError as error:
            print(error)
            print("Failed to create diary entry.")

    def get_client_plan_event(self, options):
        get_plan_event_url = self.helpers.get_api_base_url(options) + 'sensor/?user_id=me&sensor_name=planned_event_entry'
        head = {'Authorization': 'token {}'.format(self.helpers.get_client_auth_token(options)['client1'])}
        response = requests.get(get_plan_event_url, headers=head)
        filtered_response = [x for x in response.json() if x['value']['title'] == "Plan event from UI automation test client"]
        return filtered_response

    def delete_plan_event(self, options):
        plan_event_data = self.get_client_plan_event(options)
        delete_event_url = self.helpers.get_api_base_url(options) + 'sensor/' + str(plan_event_data[0]['_id']) + '/?user_id=me'
        head = {'Authorization': 'token {}'.format(self.helpers.get_client_auth_token(options)['client1'])}
        try:
            requests.delete(delete_event_url, headers=head)
        except requests.exceptions.HTTPError as error:
            print(error)
            print("Failed to delete Session.")

    def create_client_plan_event_by_therapist(self, options, status):
        plan_time = (datetime.utcnow() + timedelta(hours=2)).strftime('%Y-%m-%dT%H:%M:%SZ')
        therapist = self.helpers.get_therapist_auth_token(options)
        client = self.helpers.get_client_auth_token(options)
        create_event_url = self.helpers.get_api_base_url(options) + "sensor/?user_id={}".format(client['client1_user'])
        head = {'Authorization': 'token {}'.format(therapist['therapist2'])}
        create_event_body = [{
            "sensor_name": "planned_event_entry",
            "source_name": "goalie_2",
            "start_time": "{}".format(plan_time),
            "end_time": "{}".format(plan_time),
            "version": 2,
            "value": {
                "title": "Plan event from UI automation test by therapist "+status,
                "description": "This data come from python requests",
                "shouldSendNotification": False,
                "plannedFor": "{}".format(plan_time),
                "status": status,
                "activityType": "FUN_ACTIVITY"
            }
        }]
        try:
            requests.post(create_event_url, headers=head, json=create_event_body)
        except requests.exceptions.HTTPError as error:
            print(error)
            print("Failed to create plan event.")

    def get_client_plan_event_by_therapist(self, options, status):
        get_plan_event_url = self.helpers.get_api_base_url(
            options) + 'sensor/?user_id=me&sensor_name=planned_event_entry'
        head = {'Authorization': 'token {}'.format(self.helpers.get_client_auth_token(options)['client1'])}
        response = requests.get(get_plan_event_url, headers=head)
        filtered_response = [x for x in response.json() if x['value']['title'] == "Plan event from UI automation test by therapist "+status]
        return filtered_response

    def delete_plan_event_by_therapist(self, options, status):
        plan_event_therapist_data = self.get_client_plan_event_by_therapist(options, status)
        delete_event_url = self.helpers.get_api_base_url(options) + 'sensor/' + str(
            plan_event_therapist_data[0]['_id']) + '/?user_id=me'
        head = {'Authorization': 'token {}'.format(self.helpers.get_client_auth_token(options)['client1'])}
        try:
            requests.delete(delete_event_url, headers=head)
        except requests.exceptions.HTTPError as error:
            print(error)
            print("Failed to delete Session.")

    def create_invitation_from_client(self, options):
        network_url = self.helpers.get_api_base_url(options) + 'network/'
        therapist_login = self.helpers.get_static_therapist1(options)
        create_network_head = {'Authorization': 'token {}'.format(self.helpers.get_client_auth_token(options)['client2'])}
        create_network_body = {'creator_role': 'patient', 'invitations': [{'email': '{}'.format(therapist_login['email']), 'invitation_type': 'invite_user_to_network', 'network_role': 'therapist'}]}
        try:
            requests.post(network_url, headers=create_network_head, json=create_network_body)
        except requests.exceptions.HTTPError as error:
            print(error)
            print("Invitation failed.")

    # Edit client's birthday
    def edit_client_birthday(self, options, birthday):
        # Check birthday option
        if birthday == "today":
            birthdate = (datetime.now() - timedelta(365.25*25)).strftime('%Y-%m-%d')
        else:
            birthdate = ((datetime.now() - timedelta(365.25*25)) + timedelta(1)).strftime('%Y-%m-%d')
        profile_url = self.helpers.get_api_base_url(options) + 'profile/me/'
        head = {'Authorization': 'token {}'.format(self.helpers.get_client_auth_token(options)['client1'])}
        try:
            requests.patch(profile_url, headers=head, data={'birth_date': birthdate})
        except requests.exceptions.HTTPError as error:
            print(error)
            print("Failed to edit birth date.")

    # Get client's meeting notes
    def get_client_meeting_notes(self, options, cache):
        get_meeting_url = self.helpers.get_api_base_url(options) + 'sensor/?user_id=me&sensor_name=meeting_note'
        head = {'Authorization': 'token {}'.format(self.helpers.get_client_auth_token(options)['client1'])}
        response = requests.get(get_meeting_url, headers=head)
        filtered_response = [x for x in response.json() if x['value']['title'] == str(cache.get("web-goalie/created-meeting-title", None))]
        return filtered_response

    # Delete created meeting note
    def delete_meeting_note(self, options, cache):
        meeting_data = self.get_client_meeting_notes(options, cache)
        delete_event_url = self.helpers.get_api_base_url(options) + 'sensor/' + str(meeting_data[0]['_id']) + '/?user_id=me'
        head = {'Authorization': 'token {}'.format(self.helpers.get_client_auth_token(options)['client1'])}
        try:
            requests.delete(delete_event_url, headers=head)
        except requests.exceptions.HTTPError as error:
            print(error)
            print("Failed to delete Session.")

    def gscheme_step1_completed_by_client(self, options, cache):
        cache.set("web-goalie/gscheme_title_time", str(datetime.now()))
        cache.set("web-goalie/gscheme_time", str(datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')))
        gscheme_url = self.helpers.get_api_base_url(options) + 'sensor/?user_id=me'
        head = {'Authorization': 'token {}'.format(self.helpers.get_client_auth_token(options)['client1'])}
        gscheme_body = [{
            "sensor_name": "gscheme",
            "source_name": "goalie_2",
            "start_time": "{}".format(cache.get("web-goalie/gscheme_time", None)),
            "end_time": "{}".format(cache.get("web-goalie/gscheme_time", None)),
            "version": 2,
            "value": {
                "stage": "STEP_1_FINISHED",
                "gebeurtenis": "Event " + cache.get("web-goalie/gscheme_title_time", None),
                "gedachten": "Thought field text",
                "gedrag": "Behaviour field text",
                "gevolg": "Consequence field text"
            }
        }]
        try:
            response = requests.post(gscheme_url, headers=head, json=gscheme_body)
            cache.set("web-goalie/gscheme_id", str(response.json()[0]['_id']))
        except requests.exceptions.HTTPError as error:
            print(error)
            print("Failed to complete thought record - step 1.")

    def gscheme_step2_completed_by_client(self, options, cache):
        gscheme_url = self.helpers.get_api_base_url(options) + 'sensor/' + cache.get("web-goalie/gscheme_id", None) + '/?user_id=me'
        head = {'Authorization': 'token {}'.format(self.helpers.get_client_auth_token(options)['client1'])}
        gscheme_body = {
            "sensor_name": "gscheme",
            "source_name": "goalie_2",
            "start_time": "{}".format(cache.get("web-goalie/gscheme_time", None)),
            "end_time": "{}".format(cache.get("web-goalie/gscheme_time", None)),
            "version": 2,
            "value": {
                "stage": "STEP_2B_FINISHED",
                "gebeurtenis": "Event " + cache.get("web-goalie/gscheme_title_time", None),
                "gedachten": "Thought field text",
                "gedrag": "Behaviour field text",
                "gevolg": "Consequence field text",
                "mainThought": "Step 2 - Thought",
                "mainThoughtBelievabilityBefore": 50,
                "questions": {
                    "proofFor": "1a Proof for answer",
                    "proofAgainst": "1b Proof againts answer",
                    "worst": "2 Worst answer",
                    "prosCons": "3 Pros Cons answer",
                    "differentView": "4 Different view answer",
                    "sayToSomeone": "5 Say to someone answer",
                    "sayBackFromSomeone": "6 Say back from someone answer",
                    "futureThought": "7 Future thought answer"
                }
            }
        }
        try:
            requests.put(gscheme_url, headers=head, json=gscheme_body)
        except requests.exceptions.HTTPError as error:
            print(error)
            print("Failed to complete thought record - step 2.")

    def gscheme_step3_completed_by_client(self, options, cache):
        gscheme_url = self.helpers.get_api_base_url(options) + 'sensor/' + cache.get("web-goalie/gscheme_id", None) + '/?user_id=me'
        head = {'Authorization': 'token {}'.format(self.helpers.get_client_auth_token(options)['client1'])}
        gscheme_body = {
            "sensor_name": "gscheme",
            "source_name": "goalie_2",
            "start_time": "{}".format(cache.get("web-goalie/gscheme_time", None)),
            "end_time": "{}".format(cache.get("web-goalie/gscheme_time", None)),
            "version": 2,
            "value": {
                "stage": "STEP_3B_FINISHED",
                "gebeurtenis": "Event " + cache.get("web-goalie/gscheme_title_time", None),
                "gedachten": "Thought field text",
                "gedrag": "Behaviour field text",
                "gevolg": "Consequence field text",
                "mainThought": "Step 2 - Thought",
                "mainThoughtBelievabilityBefore": 50,
                "questions": {
                    "proofFor": "1a Proof for answer",
                    "proofAgainst": "1b Proof againts answer",
                    "worst": "2 Worst answer",
                    "prosCons": "3 Pros Cons answer",
                    "differentView": "4 Different view answer",
                    "sayToSomeone": "5 Say to someone answer",
                    "sayBackFromSomeone": "6 Say back from someone answer",
                    "futureThought": "7 Future thought answer"
                },
                "alternativeThought": "Step 3 - Alternative thought",
                "alternativeThoughtBelievability": 55,
                "mainThoughtBelievabilityAfter": 60
            }
        }
        try:
            requests.put(gscheme_url, headers=head, json=gscheme_body)
        except requests.exceptions.HTTPError as error:
            print(error)
            print("Failed to complete thought record - step 3.")

    def delete_sensor(self, options, sensor_id):
        gscheme_url = self.helpers.get_api_base_url(options) + 'sensor/' + sensor_id + '/?user_id=me'
        head = {'Authorization': 'token {}'.format(self.helpers.get_client_auth_token(options)['client1'])}
        try:
            requests.delete(gscheme_url, headers=head)
        except requests.exceptions.HTTPError as error:
            print(error)
            print("Failed to delete Sensor.")

    def create_extra_therapist_invitation(self, options):
        try:
            head_therapist1 = {'Authorization': 'token {}'.format(self.helpers.get_therapist_auth_token(options)['therapist1'])}
            head_therapist2 = {'Authorization': 'token {}'.format(self.helpers.get_therapist_auth_token(options)['therapist2'])}

            # send invitation
            send_invitation_url = self.helpers.get_api_base_url(options) + 'invitation/'
            send_invitation_body = {
                "email": self.helpers.get_static_therapist2(options)['therapist2']['email'],
                "invitation_type": "invite_user_to_network",
                "network_role":"therapist",
                "network_id": self.helpers.get_static_network_id(options)
            }

            response = requests.post(send_invitation_url, headers=head_therapist1, json=send_invitation_body)
            invitation_id = str(response.json()['id'])

            # # get key invitation
            get_invitation_url = self.helpers.get_api_base_url(options) + 'invitation/' + invitation_id + '/'
            response = requests.get(get_invitation_url, headers=head_therapist2)
            key_approval = str(response.json()['key'])

            # # accept invitation
            accept_invitation_url = self.helpers.get_api_base_url(options) + 'invitation/accept-invite/' + key_approval
            requests.post(accept_invitation_url, headers=head_therapist2)

        except requests.exceptions.HTTPError as error:
            print(error)
            print("Failed to send the invitation")

    def create_session_plan(self, options, cache):
        current_time = cache.get("web-goalie/completed-session-date", None)
        card_title = 'Session completed ' + current_time
        create_event_url = self.helpers.get_api_base_url(options) + 'sensor/?user_id=me'
        head = {'Authorization': 'token {}'.format(self.helpers.get_client_auth_token(options)['client1'])}
        plan_time = (datetime.utcnow() + timedelta(hours=2)).strftime('%Y-%m-%dT%H:%M:%SZ')
        create_event_body = [{
            "sensor_name": "planned_event_entry",
            "source_name": "goalie_2",
            "start_time": "{}".format(plan_time),
            "end_time": "{}".format(plan_time),
            "version": 3,
            "value": {
                "title": card_title,
                "description": "This data come from python requests",
                "shouldSendNotification": False,
                "plannedFor": "{}".format(plan_time),
                "status": "COMPLETED",
                "activityType": "THERAPY_SESSION"
            }
        }]

        try:
            response = requests.post(create_event_url, headers=head, json=create_event_body)
            cache.set("web-goalie/session_id", str(response.json()[0]['_id']))
        except requests.exceptions.HTTPError as error:
            print(error)
            print("Failed to create Therapy Session.")
