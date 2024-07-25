from __future__ import annotations

from astropy.table import Table, Row
from subprocess import getstatusoutput
from multiprocessing.pool import ThreadPool
from pathlib import Path
from io import StringIO

from .inventory import Inventory
from .email import BasicMailer

from html2text import html2text
import sys
import argparse

import socket

from .dataclasses import strictdataclass, Field
from pydantic.networks import IPvAnyAddress
from typing import ClassVar, Annotated

PortType = Annotated[int, Field(ge=1, le=65535)]

def check_any_port(ip: IPvAnyAddress, ports: list[PortType]):
    """Check if any port from a list is open for a given IP Address"""

    for port, proto in ports:

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.2)
            connected = not sock.connect_ex((str(ip), port))
            sock.close()
            if connected:
                return True 

        except Exception as e:
            print(f'socket error for {ip} on port {port}: {e}')
            break

        return 

@strictdataclass(frozen=False)
class Device:

    ip:         IPvAnyAddress
    location:   str 
    hwid:       str 
    on:         bool | None = None
    ping:       bool | None = None 
     
    def __iter__(self):
        for x in self.__dataclass_fields__:
            yield gettattr(self, x.name)

    @classmethod
    def names(self):
        return [f.name for f in self.__dataclass_fields__]

    def update_status(self):
        self.ping = not getstatusoutput(f'ping -c1 -w2 {self.ip}')[0]
        self.on = self.ping

    @classmethod
    def from_row(cls, row: dict | Row) -> DeviceStatus:

        ip, location, hwid = row['ip'] , row['location'], row['hwid']
        
        kind = row['device_type']
        
        for subcls in self.subclasses():
            if kind == subcls.__name__:
                cls = subcls
                break
        else:
            cls = DeviceStatus 

        return cls(ip=ip, location=location, hwid=hwid)

@strictdataclass(frozen=False)
class IPPower(Device):
    ...

@strictdataclass(frozen=False)
class Camera(Device):
    ...

@strictdataclass(frozen=False)
class Mount(Device):
    ...

@strictdataclass(frozen=False)
class Focuser(Device):
    ...

@strictdataclass(frozen=False)
class PC(Device):

    http:       bool | None = None
    vnc:        bool | None = None
    anydesk:    bool | None = None
    HTTP_PORTS:    ClassVar[list[PortType]] = [80, 443]
    VNC_PORTS:     ClassVar[list[PortType]] = [5800, 5900]
    ANYDESK_PORTS: ClassVar[list[PortType]] = [80, 443]

    def get_status(self):

        x = self.copy()
        x.update_status()
        return x

    def update_status(self):

        super().update_status()

        self.http = check_any_ports(ip, cls.HTTP_PORTS)
        self.vnc = check_any_ports(ip, cls.VNC_PORTS)
        self.anydesk = check_any_port(ip, cls.ANYDESK_PORTS) 
        self.on = self.ping or self.http or self.vnc or self.anydesk
    
def location_abbr(l: str) -> str:
    
    if 'Building' in l:
        return l.split(' ')[1]

    if 'HAT' in l:
        return 'H'
    
    if l == 'ATLAS DOME':
        return 'A'

    if 'Container' in l:
        return l[0] + 'C'

    if l == 'Control Room':
        return 'CR'

    return l

def list_devices(
    device_types: list[str] = ['PC', 'Router'], 
    locations: list[str] = [],
    hwid: str = '',
) -> list[DeviceType]:

    inventory = Inventory(user='generic_obstech')
    tab = inventory.devices(keep_unused=False)

    tab['Location'] = [location_abbr(l) for l in tab['Location']]

    if hwid:
        tab = tab[[hwid in id for id in tab['HWID']]]

    if device_types:
        tab = tab[[d in device_types for d in tab['Device Type']]]

    if locations:
        tab = tab[[l in locations for l in tab['Location']]]

    return [DeviceType.from_row(t) for t in tab]

def load_ips(
    device_types: list[str] = ['PC', 'Router'], 
    locations: list[str] = [],
    hwid: str = '',
) -> Table:

    inventory = Inventory(user='generic_obstech')
    tab = inventory.devices(keep_unused=False)

    tab['Location'] = [location_abbr(l) for l in tab['Location']]

    if hwid:
        tab = tab[[hwid in id for id in tab['HWID']]]

    if device_types:
        tab = tab[[d in device_types for d in tab['Device Type']]]

    if locations:
        tab = tab[[l in locations for l in tab['Location']]]

    return tab

def report_connection(
    ip: str, 
    ports: list[tuple[int, str]] = [
        (80,  'HTTP'),          # HTTP 
        (139, 'netbios-ssn'),   # Netbios SSN
        (443, 'https'),         # HTTPS 
        (445, 'microsofts-ds'), # Microsoft DS
        (5800, 'vnc-http'),     # vnc on web
        (5900, 'vnc'),          # vncviewer
        (6568, 'anydesk'),      # anydesk
    ]
):
    
    # check ping
    connected = not getstatusoutput(f'ping -c1 -w2 {ip}')[0]
    if connected:
        return 'up (ping)'
       
    # check selected ports: typical networking + anydesk & vncviewer
    for port, proto in ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.2)
            connected = not sock.connect_ex((ip, port))
            if connected:
                return f'up ({port}/{proto})'
            sock.close()
        except Exception as e:
            print(f'socket error for {ip}: {e}')
            break

    return 'down'

def report_all_connections(tab, nthreads=20):

    ips = tab['IP']
    pool = ThreadPool(processes=nthreads)
    connections = list(pool.imap(report_connection, ips))

    up = [c != 'down' for c in connections]

    tab.add_columns([connections, up], names=['Connection', 'up'])
   
def list_computers():
    
    # parse arguments
    
    parser = argparse.ArgumentParser(
        description="Scan PCs to check if they are up and answering to various protocols."
    )
    parser.add_argument(
        "-l",
        nargs="+",
        default=[],
        metavar="DEV",
        help="Locations of device in short form (1 = Building 1, AC = Atlas container)"
    )
    parser.add_argument(
        "--hwid",
        default=None,
        metavar="HWID",
        help="Expression contained in HWID"
    )
    parser.add_argument(
        "--nthreads",
        metavar="N",
        type=int,
        default=20,
        help="Number of simultaneous checks"
    )
    parser.add_argument(
        "-d",
        default=False,
        action="store_true",
        help="Report only down machines",
    )
    parser.add_argument(
        "--email",
        nargs="*",
        default="",
        help="Email to send results to"
    )
    args = parser.parse_args()
    
    # Look for all PCs matching criteria

    pcs = list_devices(
        device_types=['PC'], 
        locations=args.l,
        hwid=args.hwid,
    )
    pcs = sorted(pcs, key = lambda pc: (pc.location, pc.hwid))
    
    # Get status

    pool = ThreadPool(processes=nthreads)
    pcs = pool.imap(Device.get_status, pcs)

    # Print it as a table
    tab = Table(rows=[list(pc) for pc in pcs], names=PC.names())
    tab.sort(['up', 'Location', 'HWID'])
    
    ntot = len(tab)
    nup = sum(tab['on'])
    ndown = ntot - ndown

    if args.d:
        tab = tab[tab['on'] == False]
   
    tab.columns['Location'].name = 'Loc.'
    print(f'{ndown} computers of {ntot}')
    tab.pprint(max_lines=9999,max_width=999) 

def main_script():

    # parse arguments
    
    parser = argparse.ArgumentParser(
        description="Scan client devices to check if they are up."
    )
    parser.add_argument(
        "-t",
        nargs="+",
        default=["PC", "Server"],
        metavar="DEV",
        help="Type of device (PC, server, IPPower, etc.)"
    )
    parser.add_argument(
        "-l",
        nargs="+",
        default=[],
        metavar="DEV",
        help="Locations of device in short form (1 = Building 1, AC = Atlas container)"
    )
    parser.add_argument(
        "--hwid",
        default=None,
        metavar="HWID",
        help="Expression contained in HWID"
    )
    parser.add_argument(
        "--nthreads",
        metavar="N",
        type=int,
        default=20,
        help="Number of simultaneous checks"
    )
    parser.add_argument(
        "-d",
        default=False,
        action="store_true",
        help="Report only down machines",
    )
    parser.add_argument(
        "--email",
        nargs="*",
        default="",
        help="Email to send results to"
    )
    args = parser.parse_args()
    
    # inquire all IPs

    tab = load_ips(
        device_types=args.t, 
        locations=args.l,
        hwid=args.hwid,
    )

    tab.sort(['Location', 'HWID'])
    report_all_connections(tab, nthreads=args.nthreads)
  
    # format report
    
    ndev = len(tab)
    nup = sum(tab['up'])
    ndown = ndev - nup

    if args.d:
        tab = tab[tab['up'] == False]
    tab.sort(['up', 'Location', 'HWID'])
        
    names = ['HWID', 'Location', 'IP', 'Name', 'Connection']
    tab = tab[names]
 
    subject = f"El Sauce devices report: {ndown} of {ndev} are down"

    html = "<html><head></head><body>\n"   
    html += f"<p>The report was generated with</p>\n<ul>\n"
    html += f"<li>command: <kbd>{sys.argv[0]}</kbd></li>\n"
    html += f"<li>device type(s): {', '.join(args.t)}</li>\n"
    html += f"<li>location(s): {', '.join(args.l) if args.l else 'all'}</li>\n"
    html += f"<li>hardware ID contains: {args.hwid if args.hwid else '<any string>'}</li>\n"
    html += "</ul>\n\n"

    if args.d and not len(tab):
        html = "<p>All devices are up</p>"
    else:
        s = StringIO()
        tab.write(s, format='html')
        html += s.getvalue()
    html += "\n\n</body></html>"

    # send email

    if args.email:
        
        username = 'regis.lachaume@gmail.com'
        with BasicMailer.from_credentials(user='device_status') as mailer:
            to, *cc = args.email
            mailer.send(subject=subject, content=html, to=to, cc=cc)

    # write to console
    print(subject)
    print()
    tab.columns['Location'].name = 'Loc.' 
    tab.pprint(max_lines=9999, max_width=999)
 
