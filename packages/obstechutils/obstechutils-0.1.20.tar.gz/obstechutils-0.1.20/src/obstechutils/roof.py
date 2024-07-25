from __future__ import annotations

from .db import DataBase
from pydantic import NonNegativeInt, FiniteFloat
import mysql.connector
from mysql.connector.cursor import MySQLCursor

from .dataclasses import strictdataclass

class InexistentRoofError(Exception):
    ...

@strictdataclass
class RoofInfo:

    roof_index: NonNegativeInt
    roof_name: str
    mqtt_open_cmd: str 
    mqtt_close_cmd: str
    mqtt_status_cmd: str
    mqtt_get_status_cmd: str
    open_delay: NonNegativeInt
    close_delay: NonNegativeInt
    set_manual_cmd: str
    stop_manual_cmd: str
    open_manual_cmd: str
    close_manual_cmd: str
    sunset_limit: FiniteFloat
    sunrise_limit: FiniteFloat
    telegram_token: str

    @classmethod
    def from_db(cls, roof_index: int) -> RoofInfo:

        roof_query = cls.ROOF_QUERY 
        roof_query += f"WHERE RoofIndex = '{roof_index}'"

        db = DataBase.from_credentials('ElSauceRoofs', user='generic_obstech')
        with db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(roof_query)
            res = cursor.fetchall()

        if len(res):
            return cls(*res[0])

        msg = f"No such roof index in database: {roof_index}"
        raise InexistentRoofError(msg) 

    @classmethod
    def all_from_db(cls) -> list[RoofInfo]:
        
        roof_query = cls.ROOF_QUERY
        roof_query += f"ORDER BY RoofIndex"

        db = DataBase.from_credentials('ElSauceRoofs', user='generic_obstech')
        with db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(roof_query)
            res = cursor.fetchall()

        return [cls(*item) for item in res]
    
RoofInfo.ROOF_QUERY: str = """
    SELECT 
        RoofIndex, RoofName, 
        mqtt_open_cmd, mqtt_close_cmd, mqtt_status_cmd, mqtt_get_status_cmd, 
        open_delay, close_delay,
        set_manual_cmd, stop_manual_cmd, open_manual_cmd, close_manual_cmd,
        sunset_limit, sunrise_limit, 
        TelegramToken
    FROM `RoofsParams`
"""

def list_roofs():

    from astropy.table import Table

    roofs = RoofInfo.all_from_db()

    names = list(roofs[0].__dataclass_fields__.keys())

    rows = [tuple(getattr(roof, p) for p in names) for roof in roofs]

    tab = Table(rows=rows, names=names)
    tab.pprint_all()
