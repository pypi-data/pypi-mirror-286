from astropy import time, coordinates
from typing_extensions import Annotated
import queue

from .dataclasses import autoconverted, Field

TimeType = autoconverted(time.Time)
TimeDeltaType = autoconverted(time.TimeDelta)
PortType = Annotated[int, Field(ge=0, lt=65535)]
QOSType = Annotated[int, Field(ge=0, le=2)]
EarthLocationType = autoconverted(coordinates.EarthLocation)
SkyCoordType = autoconverted(coordinates.SkyCoord)
QueueType = autoconverted(queue.Queue)

try:
    from typing import TypeAlias
except:
    TypeAlias = type

