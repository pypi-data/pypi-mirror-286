from __future__ import annotations

import requests
from .db import DataBase
from .credentials import Credentials
from typing import Union,Dict
from .dataclasses import strictdataclass 

@strictdataclass
class TelegramBroadcastBot:

    token: str
    database: str
    recipients_table: str
    recipients_id_column: str 
    recipients_name_column: str = 'Name'
    user: str = 'generic_obstech'

    @classmethod
    def from_credentials(
            cls, 
            user: str = 'generic_obstech'
    ) -> TelegramBroadcastBot:

        creds = Credentials.load('telegram',user=user) 
        token = creds['token']
        del creds['token']

        return cls(token=token, **creds)
   
    def select_users(self, user_criteria: Dict[str, object] = {}) -> list[str]:

        query = f"""
            SELECT {self.recipients_id_column} {self.recipients_name_column}
            FROM {self.recipients_table}
        """
        if user_criteria:
            criteria = ["{k} = {repr(v)}" for k, v in user_criteria]
            criteria = "\nAND ".join(criteria)
            query += f"WHERE {criteria}"

        db = DataBase.from_credentials(self.database, user=self.sql_user)
        with db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            res = cursor.fetch_all()

        return res

    def send_message(
        self, 
        message: str, 
        id: str, 
        /, *,
        name: str = 'user',
        error_id: str = '', 
    ):

        req_url = (
            f"https://api.telegram.org/bot{self.token}/"
            f"sendMessage?parse_mode=Markdown&chat_id={id}&text={message}"
        )
        res = requests.get(req_url)
       
        # report error to another user if error_id is provided 
        if not res.json()['ok']:
            error_message = f"Error sending message to {name} ID={id}: {res}"
            print(error_message)
            if error_id:
                self.send_message(error_message, id=error_id)

    def broadcast(
        self, 
        message: str, 
        /, *,
        user_criteria: Dict[str,object] = {},
        error_id: str = 260757924, # perhaps caller should state it instead
    ) -> None:
   
        users = self.select_users(user_criteria)
        for id, name in users:
            self.send_message(message, id, name, error_id=error_id) 
        
