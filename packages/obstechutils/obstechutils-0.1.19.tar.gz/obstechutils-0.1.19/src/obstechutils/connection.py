from abc import ABC, abstractmethod
from pydantic import (
    IPvAnyAddress, PositiveFloat, NonNegativeFloat, PositiveInt, NonNegativeInt
)

from serial import Serial, EIGHTBITS, PARITY_NONE, STOPBITS_ONE
from serial.tools.list_ports import comports as list_serial_ports
from serial.tools.list_ports_common import ListPortInfo

from socket import socket
from socket import AF_INET, SOCK_STREAM, SHUT_RDWR, MSG_PEEK, MSG_DONTWAIT

import select

from .dataclasses import dataclass
from .types import PortType

@dataclass(kw_only=True, frozen=True)
class Connection(ABC):
    """Base class for connections over serial port or INET (socket)"""

    # dataclass is fixed except for that _conn keyword
    def _set_connection(self, value: object) -> None:
        object.__setattr__(self, '_conn', value)
        
    def __post_init__(self):
        self._set_connection(None)
        if self.autoconnect:
            self.connect()

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, _a, _b, _c):
        self.disconnect()

    def disconnect(self):
        if self._conn is not None:
            self._disconnect()
            self._set_connection(None)

    def reconnect(self) -> None:
        self.disconnect()
        self.connect() 

    def connect(self) -> None:
        
        if self._conn is not None:
            if not self._is_connection_ok():
                self.disconnect()
                
        if self._conn is None:
            self._connect() 
    
    def receive(self, *, start: str = '', end: str = '', size: int = 96) -> str:

        try:

            if start:
                start = start.encode(self.encoding)
                self._receive_until(delim=start, buffer_size=size)

            if end:
                end = end.encode(self.encoding)
                answer = self._receive_until(delim=end, buffer_size=size)
                answer = answer.removesuffix(end)
            else:
                answer = self._receive_fixed(size=size)
        
        except AttributeError:
            raise ConnectionError('cannot send to inexistent connection')

        return answer.decode(self.encoding)
    
    def send(
        self, message: str, /, *, 
        start: str = '', end: str = ''
    ) -> None:

        message = f"{start}{message}{end}".encode(self.encoding)
        try: 
            return self._send(message)
        except AttributeError:
            raise ConnectionError('cannot read from inexistent connection')

    @abstractmethod
    def _connect(self) -> None: ...
    
    @abstractmethod
    def _disconnect(self) -> None: ...

    @abstractmethod
    def _is_connection_ok(self) -> bool: ...

    @abstractmethod
    def _receive_until(self, *, delim: str, buffer_size: int) -> str:  ...

    @abstractmethod
    def _receive_fixed(self, *, size: int) -> str: ...

    @abstractmethod
    def _send(self, message: bytes) -> None: ...

    @abstractmethod
    def flush_input(self) -> None: ...
   
@strictdataclass
class INETConnection(Connection):
    """Handle socket connections"""
   
    host: IPvAnyAddress
    port: PortType
    encoding: str = 'ascii'
    timeout: PositiveFloat = 1.0

    def _disconnect(self) -> None:
        try:
            self._conn.shutdown(SHUT_RDWR)
        except:
            ...
        self._conn.close()

    def _is_connection_ok(self) -> bool:

        conn = self._conn

        try:
            _, _, err = select.select([conn,], [conn,], [conn], self.timeout)
            conn.send(b'')
        except:
            return False

        if err:
            return False

        return True

    def _socket_recv(self, n: PositiveInt) -> bytes:

        r = self._conn.recv(n)

        if len(r):
            return r

        raise BrokenPipeError('Socket connection broken')

    def _socket_send(self, msg: bytes) -> int:

        totalsent = 0
        while totalsent < len(msg):
            sent = self._conn.send(msg[totalsent:])
            if sent == 0:
                raise ConnectionError("socket connection broken")
            totalsent += sent

        return totalsent

    def _connect(self) -> None:
        
        conn = socket(family=AF_INET, type=SOCK_STREAM)
        conn.settimeout(self.timeout)
        conn.connect((str(self.host), self.port))
        self._set_connection(conn)
        
    def _receive_until(self, delim: bytes, buffer_size: PositiveInt) -> bytes: 
       
 
        answer = b''
        while not answer.endswith(delim):

            peeked = self._conn.recv(buffer_size, MSG_PEEK)

            nread = buffer_size
            if delim in peeked:
                nread = peeked.index(delim) + len(delim)

            answer += self._socket_recv(nread)

        return answer 

    def _receive_fixed(self, size: PositiveInt) -> bytes:
        
        answer = b''
        while missing := size - len(answer):
            answer += self._socket_recv(missing)

        return answer

    def _send(self, message: bytes) -> None:

        return self._socket_send(message)

    def _ok_to_read(self, timeout: PositiveFloat = 0.000001) -> bool:

        ok, _, _ = select.select([self._conn], [], [], timeout)

        return bool(ok)

    def receive_all(self, buffer_size: PositiveInt = 128) -> None:
        
        answer = b''
        while self._ok_to_read():
            answer += self._socket_recv(buffer_size)

        return answer.decode(self.encoding)
    
    def flush_input(self, buffer_size: PositiveInt = 128) -> None:

        while self._ok_to_read():
            self._socket_recv(buffer_size)

@strictdataclass
class SerialConnection(Connection):
    """Handle connections to serial port"""
    
    vendor_id: NonNegativeInt = 0
    product_id: NonNegativeInt = 0
    serial_number: str = '' 
    encoding: str = 'ascii'
    baudrate: PositiveInt = 9600
    bytesize: PositiveInt = EIGHTBITS
    stopbits: PositiveInt = STOPBITS_ONE
    timeout: NonNegativeFloat = 1.0
    write_timeout: NonNegativeFloat = 0
    inter_byte_timeout: NonNegativeFloat = 0
    exclusive: bool = False
    xonxoff: bool = False
    
    def _is_connection_ok(self):
        
        conn = self._conn

        try:
            _, _, err = select.select([conn,], [conn,], [conn], self.timeout)
        except:
            return False

        if err:
            return False

        return True
    
    def _disconnect(self) -> None:
        self._conn.close()

    def _connect(self):

        port = self.find_port()
        if port is None:
            msg = f'Serial device not found'
            raise ConnectionError(msg)
       
        if write_timeout == 0:
            write_timeout = None
        if inter_byte_timeout == 0:
            inter_byte_timeout = None
 
        conn = Serial(
            port.device, 
            baudrate=self.baudrate, exclusive=self.exclusive,
            bytesize=self.bytesize, stopbits=self.stopbits,
            parity=PARITY_NONE,
            timeout=self.timeout, write_timeout=write_timout, 
            inter_byte_timeout=inter_byte_timout,
            xonxoff=self.xonxoff
        ) 
        self._set_connection(conn)

    def find_port(self) -> ListPortInfo:
            
        ports = list_serial_ports()
        for port in ports:
            if self._is_correct_port(port):
                return port
            
        return None

    def _is_correct_port(self, port: ListPortInfo) -> bool:

        if self.vendor_id and port.vid != self.vendor_id:
            return False
        if self.product_id and port.pid != self.product_id:
            return False
        if self.serial_number and port.serial_number != self.serial_number:
            return False

        return True

    def _receive_until(
        self, delim: bytes, buffer_size: PositiveInt = 128
    ) -> bytes:

        return self._conn.read_until(delim)

    def _receive_fixed(self, size: PositiveInt = 128) -> bytes:
                
        return self._conn.read(size)

    def _send(self, message: bytes) -> None:

        self._conn.write(message)
    
    def flush_input(self, buffer_size: PositiveInt = 128) -> None:

        self._conn.flushInput()
