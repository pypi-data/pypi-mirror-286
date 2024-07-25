from astropy import time
from typing_extensions import Annotated

from .dataclasses import autoconverted, Field

TimeType = autoconverted(time.Time)
TimeDeltaType = autoconverted(time.TimeDelta)
PortType = Annotated[int, Field(ge=0, lt=65535)]
QOSType = Annotated[int, Field(ge=0, le=2)]
