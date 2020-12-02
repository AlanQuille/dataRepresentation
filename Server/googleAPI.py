#Copyright 2018 Google LLC
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
import json
from datetime import date
import datetime
from email.utils import parsedate_tz, mktime_tz, formatdate
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def googleAPI():
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

    # Call the Gmail API
  #  results = service.users().messages().list(userId='me').execute()
    response= service.users().messages().list(userId='me').execute()
   # print(results)
    messages =[]
    if 'messages' in response:
        messages.extend(response['messages'])
    
    while 'nextPageToken' in response:
        page_token = response['nextPageToken']
        response = service.users().messages().list(user_id='me', q=query, pageToken=page_token).execute()
        messages.extend(response['messages'])

#    for message in messages:
 #       print(message['id'])

    
    subject_list = []
    
    for i in range(0, len(messages)):
        true_or_false = 0
        today = date.today()
        completeMessage = service.users().messages().get(userId='me', id = messages[i]['id']).execute()
    #    print(today)
        headers= completeMessage['payload']['headers']
        for header in headers:
            #print(header['name'])
            if(header['name']=='Date'):
                header_date = header['value']
                tt = parsedate_tz(header_date)

                # make sure that a 0 is added to match format
                # of date.today()
                year = str(tt[0])
                month = str(tt[1])
                day = str(tt[2])

                if(len(month)<2):
                    month = "0" + month
                if(len(day)<2):
                    day = "0" + day
                current_date_of_mail = "{}-{}-{}".format(tt[0], tt[1], day)
     #           print(current_date_of_mail==str(today))
                if(current_date_of_mail==str(today)):
                    true_or_false = 1
                    break
               

        for header in headers:
            if(header['name']=='Subject' and true_or_false == 1):
                subject_list.append((messages[i]['id'], str(today), header['value']))
        
    #print(subject_list)
            



    with open('subjects_emails.json', 'w') as f:
        json.dump(subject_list, f, indent=4)

    #json.dump(completeMessage['payload']['headers'], f, indent=4)
    


    
   # labels = results.get('labels', [])

  #  if not labels:
  #      print('No labels found.')
 #   else:
  #      print('Labels:')
  #      for label in labels:
  #          print(label['name'])

if __name__ == '__main__':
    googleAPI()
# [END gmail_quickstart]
#© 2020 GitHub, Inc.
#Terms
#Privacy
#Security
#Status
#Help
#Contact GitHub
#Pricing
#API
#Training
#Blog
#About
