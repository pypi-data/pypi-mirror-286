from __future__ import annotations

from typing_extensions import Annotated
from pathlib import Path
from contextlib import contextmanager
from pydantic import FilePath, EmailStr, Field, PositiveInt

from email.message import EmailMessage
from smtplib import SMTP_SSL
import ssl
from html2text import html2text

from typing import Iterator, Union

import yaml

from .credentials import Credentials
from .dataclasses import strictdataclass, autoconverted
from .types import PortType

SMTPType = autoconverted(SMTP_SSL)

@strictdataclass
class BasicMailer:

    """Makes easy to send basic text/HTML emails."""

    username: EmailStr
    password: str 
    server: str
    port: PortType = 465 
    _server: SMTType = Field(default=SMTP_SSL(), repr=False)

    @classmethod
    def from_credentials(cls, user: str) -> BasicMailer:

        creds = Credentials.load('mail', user=user)
        
        return cls(**creds)

    def login(self) -> None:
        
        server = SMTP_SSL(self.server, self.port)
        server.login(self.username, self.password)
        self._server = server

    def quit(self) -> None:

        self._server.quit()

    def __enter__(self) -> BasicEmailServer:
        
        self.login()

        return self

    def __exit__(self, e_type, e_value, traceback) -> None:

        self.quit()

    def send(
        self,
        to: EmailStr, 
        subject: str,
        content: str,
        *,
        cc: list[EmailStr] = [],
        bcc: list[EmailStr] = [],
    ) -> None:

        if not self._server.sock:
            raise ConnectionError('Email server not initialised')

        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = self.username
        msg['To'] = to
        if cc:
            msg['Cc'] = cc
        if bcc:
            msg['Bcc'] = bcc

        if content[0:5] == '<html':
            msg.set_content(html2text(content))
            msg.add_alternative(content, subtype='html')
        else:
            msg.set_content(content)

        self._server.send_message(msg)

