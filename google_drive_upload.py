
from datetime import date, datetime
from http.client import responses
import os
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


folder_id = os.environ["FOLDER_ID"]
file_id = os.environ["FILE_ID"]
spreadsheet_id = os.environ["SPREADSHEET_ID"]

creds, _ = google.auth.default()

def generate_invitation(name):

    requests = [
        {
            'replaceAllText': {
                'containsText': {
                    'text': '{{fullname}}',
                    'matchCase':  'true'
                },
                'replaceText': name.fullname
            }}, {
            'replaceAllText': {
                'containsText': {
                    'text': '{{address}}',
                    'matchCase':  'true'
                },
                'replaceText': name.address,
            }
        },
        {
            'replaceAllText': {
                'containsText': {
                    'text': '{{letterdate}}',
                    'matchCase':  'true'
                },
                'replaceText': str(name.letterdate),
            }
        }, {
            'replaceAllText': {
                'containsText': {
                    'text': '{{passportno}}',
                    'matchCase':  'true'
                },
                'replaceText': name.passport_no,
            }
        },
        {
            'replaceAllText': {
                'containsText': {
                    'text': '{{dateofbirth}}',
                    'matchCase':  'true'
                },
                'replaceText': name.dob,
            }
        },
        {
            'replaceAllText': {
                'containsText': {
                    'text': '{{letter-content}}',
                    'matchCase':  'true'
                },
                'replaceText': name.desc,
            }
        }

    ]

    # year
    year = date.today().year
    try:
        # make copy of Google Docs Template file
        service = build('drive', 'v3', credentials=creds)
        responses['docs'] = service.files().copy(
            fileId=file_id,
            body={
                'name': f'{name.fullname}_invitation_letter_djc_{year}',
                'parents': [folder_id]
            }
        ).execute()

        doc_id = responses['docs'].get('id')

        # Update with new content data
        service_docs = build('docs', 'v1', credentials=creds)
        responses['docs'] = service_docs.documents().batchUpdate(
            documentId=doc_id,
            body={'requests': requests}).execute()

        service.permissions().create(
            fileId=doc_id,
            body={
                'role': 'reader',
                        'type': 'anyone'

            }
        ).execute()

    except HttpError as error:
        print(F'An error occurred: {error}')
        file = None

    return "https://docs.google.com/document/d/" + doc_id + "/export?format=pdf"


def letterOptions(letter_type, invite):

    # check if letter type is an attendee
    if letter_type == 'attendee':
        msg = '.'
        return msg

    # check if letter type is an opportunity grant recipient
    if letter_type == 'og':
        msg = f'. We have provided {invite.fullname} with a scholarship grant of ${invite.letteropt["value"]} USD for travel to the San Diego California, lodging in San Diego and a ticket to the conference.'
        return msg

    # check if letter type is a speaker
    if letter_type == 'speaker':
        msg = f' as a speaker to present a talk/tutorial with the title "{invite.letteropt["value"]}" at the conference.'
        return msg


def write_to_sheet(fullname,email,download_url):
    
    timestamp = datetime.now()
    timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")

    service = build('sheets', 'v4', credentials=creds)
    range_ = 'A2:D'
    value_input_option = 'USER_ENTERED'
    insert_data_option = 'INSERT_ROWS'
    values = [
        [timestamp, fullname,email, download_url]
    ]
    body = {
        'values': values
    }
    service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id,
        range=range_,
        valueInputOption=value_input_option,
        insertDataOption=insert_data_option,
        body=body
    ).execute()

    return "success"
