import pickle
import os.path
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


def create_service(client_secret_file, api_name, api_version, *scopes):
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None

    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(os.path.abspath('../token.pickle')):
        with open(os.path.abspath('../token.pickle'), 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                os.path.abspath('../{0}'.format(client_secret_file)), scopes)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(os.path.abspath('../token.pickle'), 'wb') as token:
            pickle.dump(creds, token)

    try:
        service = build(api_name, api_version, credentials=creds)
        return service
    except Exception as exception:
        print('Unable to connect')
        print(exception)
        return None


def media_file_upload(file_name, mime_type):
    return MediaFileUpload(file_name, mimetype=mime_type)
