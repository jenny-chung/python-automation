import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']

def create_connection():
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

    # try:
    #     service = build('drive', 'v3', credentials=creds)

    #     # Call the Drive v3 API
    #     results = service.files().list(
    #         pageSize=10, fields="nextPageToken, files(id, name)").execute()
    #     items = results.get('files', [])

    #     if not items:
    #         print('No files found.')
    #         return
    #     print('Files:')
    #     for item in items:
    #         print(u'{0} ({1})'.format(item['name'], item['id']))
    # except HttpError as error:
    #     # TODO(developer) - Handle errors from drive API.
    #     print(f'An error occurred: {error}')

    return creds


def upload_to_folder(folder_id, file_path, file_name, creds):
    """Upload a file to the specified folder and prints file ID, folder ID
    Args: Id of the folder
    Returns: ID of the file uploaded
    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    """
    # creds, _ = create_connection()

    try:
        # create drive api client
        service = build('drive', 'v3', credentials=creds)

        # create a file resource with metadata
        file_metadata = {
            'name': file_name,
            'parents': [folder_id]
        }

        # create a MediaFileUpload object for the file
        media = MediaFileUpload(file_path, resumable=True)

        # send a request to upload the file
        file = service.files().create(body=file_metadata, media_body=media,
                                      fields='id').execute()
        print(f'File "{file_name}" uploaded to Google Drive with ID: "{file.get("id")}".')
        # return file.get('id')

    except HttpError as error:
        print(f'An error occurred while uploading file "{file_name}": {error}')
        file = None

    return file

# Bulk upload files to Google Drive
def upload_files(directory_path, folder_id, creds):
    # get the list of files in the directory
    files = os.listdir(directory_path)
    print(f'{len(files)} files will be uploaded to Google Drive folder')
    count = 0

    # iterate over each file and upload it to Google Drive
    for file_name in files:
        file_path = os.path.join(directory_path, file_name)
        file = upload_to_folder(folder_id, file_path, file_name, creds)
        if (file is not None):
            count += 1

    print(f'{count} out of {len(files)} files were successfully uploaded to Google Drive folder!')


if __name__ == '__main__':
    creds = create_connection()

# ! Fill in the path to the folder you want to upload files from (from your local computer)
    directory_path = input('Please specify the path to the folder you want to upload files from: ')
    folder_id = input('Please specify the id of the Google Drive folder you want to upload to: ')
    upload_files(directory_path, folder_id, creds)