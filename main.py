# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gmail_quickstart]
from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient import errors

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
EMAIL_MAX_COUNT = 250

def processMessagePayload(payload) -> str:
    collumnNamesForExport = ["Date","From", "To", "CC"]
    valuesToExport = dict()
    newline = ""

    for part in payload:
        if part["name"] in collumnNamesForExport:
            valuesToExport[part["name"]] = part["value"]
    
    for column in collumnNamesForExport:
        newline += valuesToExport.get(column, "") + ";"

    return newline + "\n"

def saveToFile(lines):
    file1 = open("output.csv","a")
    file1.writelines(lines)


def listMessagesWithLabels(service, user_id, label_ids=[]):
    try:
        response = service.users().messages().list(userId=user_id,
                                                    maxResults=500).execute()
        messages = []
        if 'messages' in response:
            messages.extend(response['messages'])

        while 'nextPageToken' in response and len(messages) < EMAIL_MAX_COUNT:
            page_token = response['nextPageToken']

            response = service.users().messages().list(userId=user_id,
                                                        pageToken=page_token,
                                                        maxResults=500).execute()

            messages.extend(response['messages'])

        return messages
    
    except errors.HttpError as error:
        print('An error occurred: %s' % error)
    

def show_chatty_threads(service, user_id='me'):
    linesToExort = []
    messages = listMessagesWithLabels(service, user_id)

    listMessagesWithLabels
    for message in messages:
        data = service.users().messages().get(userId=user_id, id=message["id"]).execute()
        payload = data.get('payload', []).get('headers', [])
        line = processMessagePayload(payload)
        linesToExort.append(line)

        if len(linesToExort) >= EMAIL_MAX_COUNT:
            break

    saveToFile(linesToExort)    


def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    show_chatty_threads(service)

if __name__ == '__main__':
    main()

# [END gmail_quickstart]
