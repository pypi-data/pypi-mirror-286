from __future__ import annotations

from astropy.time import Time, TimeDelta
from typing import Union
from pathlib import Path

# Accept more formats than astropy.time.Time

def date_from_str(s: str) -> Time:
        
    d = s

    if ':' not in s and '-' not in s: # compact date format

        if len(s) in [7, 9, 11, 13]: # RINEX3 yyyydddHHMM format
            d = f"{s[0:4]}:{s[4:7]}"
            s = ":" + s[7:]
        elif len(s) in [8, 10, 12, 14]: # yyyymmddHHMMSS
            d = f"{s[0:4]}-{s[4:6]}-{s[6:8]}"
            s = "T" + s[8:]
            
        if len(s) == 3:
            s += "0000"
        elif len(s) == 5:
            s += "00"

        d += f"{s[0:3]}:{s[3:5]}:{s[5:7]}"

    return Time(d)

def format_date(date: Union[str, Time], fmt: str) -> str:
    """format_date(date, fmt)

Arguments

    date [string or astropy.Time]
        Date in any format readable by astropy.Time

    fmt [string]

        Desired format:
            rnx - RINEX 3 format "YYYYMMDDhhmm"
            pride - PRIDE PPP-AR format "YYYYJJJhhmm" using day-of-year
            iso - "YYYY-MM-DD"
            pdp3 - "YYYY/MM/DD"
            ymd - "YYYYMMDD"
        
    """
    if not isinstance(date, Time):
        date = Time(date)

    if fmt == 'rnx':
        return date.strftime("%Y%j%H%M")

    if fmt == 'pride':
        return date.strftime("%Y%j")

    if fmt == 'iso':
        return date.strftime("%Y-%m-%d")

    if fmt == 'pdp3':
        return date.strftime("%Y/%m/%d")

    if fmt == "ymd":
        return date.strftime("%Y%m%d")

    if fmt == "jyear":
        return date.jyear
        
    if fmt == "mjd":
        return date.mjd
    raise NotImplementedError(f"Unknown date format: {fmt}")

def _parse_frequency(frequency: TimeDelta) -> str:

    frequency = frequency.sec
    if frequency == 0:
        return ''
    if frequency <= 1 / 9950 or frequency > 99.5*86400:
        return 'OOU'
    if frequency < 0.01:
        return f"{round(0.01 / frequency):02d}C"
    if frequency < 1:
        return f"{round(1 / frequency):02d}H"
    if frequency < 55.5:
        return f"{round(frequency):02d}S"
    if frequency < 59.5 * 60:
        return f"{round(frequency / 60):02d}M"
    if frequency < 23.5 * 3600:
        return f"{round(frequency / 3600):02d}H"
        
    return f"{frequency / 86400:02d}D"

def _parse_period(period: TimeDelta) -> str:

    period = period.sec

    if period == 0:
        return ''
    if period >= 1 and period < 55.5:
        return f"{round(period):02d}S"
    if period < 59.5 * 60:
        return f"{round(period / 60):02d}M"
    if period < 23.5 * 3600:
        return f"{round(period / 3600):02d}H"
    if period < 99.5 * 86400:
        return f"{round(period / 86400):02d}D"
    if period > 365 * 86400 and period < 99.5 * 365.25 * 86400:
        return f"{round(period / (365.25 * 86400))}"
    
    return "00U"

def filedate(f: Union[str, Path]) -> Time:

    if isinstance(f, Path):
        f = f.name
    
    date = f.split('_')[2]

    return date_from_str(date)

def filepattern(
    marker: str = '',
    date: Time = Time(0, format='mjd'),
    *,  
    source: str = '',
    period: TimeDelta = TimeDelta('0s'),
    frequency: TimeDelta=  TimeDelta('0s'),
    constellation: str = '',
    datatype: str = '',
    filetype: str = 'rnx',
    version: int = 3,
) -> str:
    return filename(
        marker, date, source=source, period=period, frequency=frequency, 
        constellation=constellation, datatype=datatype, filetype=filetype, 
        version=version
    )

def filename(
    marker: str, 
    date: Time = Time(0, format='mjd'), 
    *, 
    period: TimeDelta = TimeDelta('0s'), 
    frequency: TimeDelta = TimeDelta('0s'), 
    source: str = 'R', 
    datatype: str = 'O', 
    constellation: str = 'M', 
    filetype: str = 'rnx', 
    version: int = 3
) -> Path:

    period = _parse_period(period)
    frequency = _parse_frequency(frequency)

    rnxdate = format_date(date, 'rnx') if date.mjd else None

    if version == 3:

        rnxdate = rnxdate if rnxdate else '[0-9]' * 11
        marker = marker if marker else '[A-Z]' * 4 + '[0-9]' * 2 + '[A-Z]' * 3
        period = period if period else '[0-9]' * 2 + '[YDHMU]' 
        frequency = frequency if frequency else '[0-9]' * 2 + '[DHMSZCU]'
        source = source if source else '[RSU]'
        constellation = constellation if constellation else '[GREJCISM]'
        datatype = datatype if datatype else '[ONM]'
 
        filename = f"{marker}_{source}_{rnxdate}_{period}_{frequency}_{constellation}{datatype}.{filetype}"
        return filename
    
    if version == 2:
    
        marker = marker[0:4].lower() if marker else '[a-z]' * 4
        datatype = datatype if datatype else '[omn]'

        yy = rnxdate[2:4] if rxndate else '[0-9]' * 2
        doy = rnxdate[4:7] if rnxdate else '[0-9]' * 3

        if not period or not date.mjd:
            hour = '[0a-x]'
        elif 'D' in period or 'Y' in period or period == '24H':
            hour = '0'
        else:
            hour = min(int(date.isot[11:12]), 23)
            hour = chr(ord('a') + hour)
 
        if filetype.startswith('crx'):
            datatype = 'd'
            filetype = filetype[0:4]
        elif filetype.startswith('rnx'):
            filetype = filetype[0:4] 
        
        filename = f"{marker}{doy}{hour}.{yy}o.{filetype}"

        return filename

    raise NotImplementedError('Only RINEX v2 o 3 filenames are implemented')

def file(
    marker: str, 
    date: Time, 
    *, 
    source: str = 'R', 
    period: TimeDelta, 
    frequency: TimeDelta, 
    datatype: str = 'O', 
    constellation: str = 'M', 
    filetype: str = 'rnx', 
    version: int = 3,
    path: Union[Path, str] = '.'
):

    night = date.iso[0:10]
    dir = Path(path).expanduser().absolute() / marker / night
    name = filename(marker, date, period=period,  frequency=frequency,
                constellation=constellation, datatype=datatype, 
                filetype=filetype, version=3) 

    return dir / name

def merge(files: list[Path | str]) -> str:

    for i, file in enumerate(files):

        with open(file, 'r') as stream:
            lines = stream.readlines()

        for l, line in enumerate(lines):
            if 'TIME OF FIRST OBS' in line:
                break

        time_end = lines[l+1]
        if i == 0:
            header = ''.join(lines[:l+1])
            content = ''.join(lines[l+2:])
        else:
            content += ''.join(lines[l+3:])

        merged = header + time_end + content

    return merged

