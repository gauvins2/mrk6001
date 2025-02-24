from email.mime.text import MIMEText
import os.path
import base64

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Replace with your actual credentials or how you obtain them.
# See Google's documentation for authenticating with the Gmail API.
SCOPES = ['https://www.googleapis.com/auth/gmail.compose']  # Important: Use compose scope


def get_gmail_service():
    """Shows basic usage of the Gmail API.
    If modifying these scopes, delete the file token.json.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token2.json'):
        creds = Credentials.from_authorized_user_file('token2.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)  # Download this file from Google Cloud Console
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token2.json', 'w') as token:
            token.write(creds.to_json())

    try:
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)
        return service

    except HttpError as error:
        print(f'An error occurred: {error}')
        return None

def create_message(to, subject, message_text):
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = 'your_email@gmail.com'  # Your Gmail address
    message['subject'] = subject
    raw_message = {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}
    return raw_message

def create_draft(service, message_body):
    try:
        message = create_message(message_body['to'], message_body['subject'], message_body['message'])
        # Wrap the message in a dictionary with the 'message' key
        draft = service.users().drafts().create(userId='me', body={'message': message}).execute()
        print(f'Draft created. Draft id: {draft["id"]}')
        return draft
    except Exception as e:
        print(f'An error occurred: {e}')
        return None

# Example usage:

service = get_gmail_service()
message_body = {
    'to': 'recipient@example.com',
    'subject': 'Démo programmatique',
    'message': """
Bonjour,

Ceci est un message de démonstration envoyé par un script Python. Le prochain exemple bouclera la boucle:
   . Lire les messages reçus
   . Les traiter via modèle Cloud et Local
   . Générer des réponses personnalisées

Cordialement,

Votre script Python

"""
}

create_draft(service, message_body)
