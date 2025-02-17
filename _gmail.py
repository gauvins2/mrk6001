import os.path
import base64

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def get_gmail_service():
    """Shows basic usage of the Gmail API.
    If modifying these scopes, delete the file token.json.
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
                'credentials.json', SCOPES)  # Download this file from Google Cloud Console
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)
        return service

    except HttpError as error:
        print(f'An error occurred: {error}')
        return None
def list_labels(service):
    """Lists all labels in the user's mailbox."""
    try:
        results = service.users().labels().list(userId='me').execute()
        labels = results.get('labels', [])

        if not labels:
            print('No labels found.')
            return

        print('Labels:')
        for label in labels:
            print(f"Name: {label['name']}, ID: {label['id']}")

    except HttpError as error:
        print(f'An error occurred: {error}')
def get_message_details(service, msg_id):
    """Gets the details of a specific message."""
    try:
        msg = service.users().messages().get(userId='me', id=msg_id, format='full').execute()

        headers = msg['payload']['headers']
        from_header = next((h['value'] for h in headers if h['name'] == 'From'), None)  # Sender
        to_header = next((h['value'] for h in headers if h['name'] == 'To'), None) # Receiver
        subject_header = next((h['value'] for h in headers if h['name'] == 'Subject'), None)  # Title/Subject
        date_header = next((h['value'] for h in headers if h['name'] == 'Date'), None) # Date/Time
        try:
            date_time_obj = datetime.strptime(date_header[:-6], '%a, %d %b %Y %H:%M:%S') # date in datatime
        except:
            date_time_obj = None # in case date can not be transformed to datetime

        # Decode the message body (handling different MIME types)
        body = None
        if msg['payload']['mimeType'] == 'text/plain':
            body = base64.urlsafe_b64decode(msg['payload']['body']['data']).decode()
        elif msg['payload']['mimeType'] == 'text/html':
            body = base64.urlsafe_b64decode(msg['payload']['body']['data']).decode()
        elif 'parts' in msg['payload']: #multipart emails
            for part in msg['payload']['parts']:
                if part['mimeType'] == 'text/plain':
                    body = base64.urlsafe_b64decode(part['body']['data']).decode()
                    break  # Use the first text/plain part
                elif part['mimeType'] == 'text/html':
                    body = base64.urlsafe_b64decode(part['body']['data']).decode()
                    break # use the first text/html part

        # Determine the message status (read/unread)
        is_read = 'UNREAD' not in msg['labelIds']

        return {
            'id': msg['id'],
            'threadId': msg['threadId'],
            'labels': msg['labelIds'],
            'from': from_header,
            'to': to_header,
            'subject': subject_header,
            'date': date_header,
            'date_datetime': date_time_obj,
            'body': body,
            'is_read': is_read,
            'snippet': msg['snippet']
        }

    except HttpError as error:
        print(f'An error occurred: {error}')
        return None
def list_emails_by_category(service, category_label_id, max_results=10):
    """Lists the most recent messages from a specific category."""
    try:
        query = f"label:{category_label_id}"  # The key change is here
        results = service.users().messages().list(userId='me', q=query, maxResults=max_results).execute()
        messages = results.get('messages', [])

        if not messages:
            print(f'No messages found in category: {category_label_id}')
            return

        print(f'Messages in category {category_label_id}:')
        for message in messages:
            msg_id = message['id']
            message_details = get_message_details(service, msg_id)  # Get full details
            if message_details:
                print("-" * 50)
                # print(f"ID: {message_details['id']}")
                # print(f"Thread ID: {message_details['threadId']}")
                print(f"From: {message_details['from']}")
                # print(f"To: {message_details['to']}")
                print(f"Subject: {message_details['subject']}")
                # print(f"Date: {message_details['date']}")
                # print(f"Date as datetime: {message_details['date_datetime']}")
                # print(f"Snippet: {message_details['snippet']}")
                # print(f"Body: {message_details['body'][:200] if message_details['body'] else None}...")  # Print the start of body
                # print(f"Is Read: {message_details['is_read']}")
                # print(f"Labels: {message_details['labels']}")
                the_body = message_details['body']
                print(the_body)

    except HttpError as error:
        print(f'An error occurred: {error}')

if __name__ == '__main__':
    service = get_gmail_service()
    if service:
        # 1. List labels to find the Category ID.  Uncomment this *once* to find the ID.
        # list_labels(service)  #Find the required category ID

        # 2. Once you have the Category ID, comment out list_labels() and use the function below:
        category_id = "Spam"  # Replace with the actual label ID for the category
        list_emails_by_category(service, category_id, max_results=10)

