from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials as GoogleCredentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from astropy.table import Table

from pathlib import Path

from .credentials import Credentials

class Sheets:

    def __init__(self, user: 'generic_obstech') -> None:

        creds = Credentials.load('googleapi', user=user)

        path = Path("~/.config/obstechutils").expanduser()
        token_file = path / creds['token']
        credentials_file = path / creds['credentials']
        scopes = creds['scopes'] 

        creds = None
        if token_file.exists():
            creds = GoogleCredentials.from_authorized_user_file(
                str(token_file), scopes
            )

        if not creds or not creds.valid:

            flow = InstalledAppFlow.from_client_secrets_file(
                str(credentials_file), scopes
            )
            creds = flow.run_local_server(port=0)
            with open(token_file, "w") as token:
                token.write(creds.to_json())

        service = build("sheets", "v4", credentials=creds)
        self._sheets = service.spreadsheets()

    def get(
        self, 
        sheet_id: str, 
        range_name: str, 
        has_colnames: bool = False,
        strip: bool = False
    ) -> Table:

        # obtain sheets
        sheet = self._sheets.values().get(
            spreadsheetId=sheet_id, 
            range=range_name,
            valueRenderOption='UNFORMATTED_VALUE',
            dateTimeRenderOption='SERIAL_NUMBER'
        )
        result = sheet.execute()

        # get values, don't forget google API just removes trailing empty 
        # cells!
        values = result.get("values", [])      
        ncols = max(len(r) for r in values)
        values = [r + [''] * (ncols - len(r)) for r in values]

        if strip:
            values = [
                [c.strip() if isinstance(c, str) else c for c in r]
                    for r in values
            ]

        if has_colnames:
            names = values[0]
            values = values[1:]
        else:
            names = None

        return Table(rows=values, names=names)

