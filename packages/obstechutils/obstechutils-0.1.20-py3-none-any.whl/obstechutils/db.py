from __future__ import annotations

from typing_extensions import Annotated
from pydantic.networks import IPvAnyAddress
from pydantic import Field, PositiveInt

from .credentials import Credentials
from .dataclasses import strictdataclass 
from .types import PortType

import mysql.connector
from mysql.connector import MySQLConnection

from contextlib import contextmanager
import yaml 
from pathlib import Path

from typing import Iterator

@strictdataclass
class DataBase: 
    """Connect to the Obstech MySQL database

USE:
    
    db = DataBase.from_credentials(database_name, user=user)
    with db.connect() as conn
        cursor = conn.cursor()
        cursor.execute(query)
        res = cursor.fetchall()

    will deal with connecting/disconnecting from the database and getting
    credentials from a credentials file.
  
CREDENTIALS FILE

    A YAML file containing the connection information:

    mysql:
        user:
            username: xxx
            password: xxx
            server:   xxx.xxx.xxx.xxx
            port:     nnnn 
 
    """    
    username: str
    password: str
    database: str 
    server: IPvAnyAddress
    port: PortType = 3306

    @classmethod
    def from_credentials(cls, user: str, **kwargs) -> DataBase:

        creds = Credentials.load('mysql', user=user)
        return cls(**creds, **kwargs)

    @contextmanager
    def connect(self) -> Iterator[MySQLConnection]:

        server = str(self.server)

        conn = mysql.connector.connect(
            host=server,
            database=self.database,
            user=self.username,
            password=self.password,
            port=self.port,
        )
        
        try:
            yield conn
        finally:
            conn.close() 
