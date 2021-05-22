from __future__ import print_function
import datetime as dt
import json
import os.path
import time
import pandas as pd
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']
file_id = '1YOE9taWHi8DbR56bv9LnOfm7CnKoRkfu'


def main():
    print('''  _____              _   _  __ _           
 |  __ \            | | (_)/ _(_)          
 | |  | |_ __   ___ | |_ _| |_ _  ___ _ __ 
 | |  | | '_ \ / _ \| __| |  _| |/ _ \ '__|
 | |__| | | | | (_) | |_| | | | |  __/ |   
 |_____/|_| |_|\___/ \__|_|_| |_|\___|_|   
                                           
                                           ''')

    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('drive', 'v3', credentials=creds)
    folder_id = '16b9IpqVclJJGxzllyG7qixKJCnYFKSdZ'
    qr = f"parents='{folder_id}'"

    now = dt.datetime.now()
    now_date = now.date()
    today_date = str(now_date)
    # print(today_date)

    results = service.files().list(orderBy="modifiedTime desc,name", pageSize=100,
                                   fields="nextPageToken, files(id, name,mimeType, "
                                          "lastModifyingUser,createdTime)").execute()
    items = results.get('files', [])
    # print(items)

    relevant_data = []

    for x in items:
        if x["createdTime"].startswith(today_date):
            relevant_data.append(x)
            finaljson = {"data": relevant_data}
            finaldata = pd.DataFrame(relevant_data)
            print(finaldata[['name', 'createdTime']])
            with open("data_file.json", "w") as write_file:
                json.dump(finaljson, write_file)

    if not relevant_data:
        print("No data found")

    time.sleep(21600)


if __name__ == '__main__':
    while True:
        main()
