"""
    _summary_

_extended_summary_

:raises IrcDisconnectError: _description_
:raises IrcDisconnectError: _description_
:raises IrcDisconnectError: _description_
:raises IrcDisconnectError: _description_
:raises IrcDisconnectError: _description_
:return: _description_
:rtype: _type_
"""
from typing import Callable
import socket
import select
import ssl
import time
import certifi

class IrcDisconnectError(Exception):
    """
    IrcDisconnectError _summary_

    _extended_summary_

    :param Exception: _description_
    :type Exception: _type_
    """

class IrcController():
    """ IRC Conroller

        :param server: address to IRC server
        :type server: str

        :param port: IRC server port
        :type port: int

        :param pingwait: keep alive delay 
        :type ping: int
    """
    def __init__(self, server: str, port: int, SSL:bool = False, pingwait: int = 300) ->  None:
        # Populate values
        self._server: str = server
        self._port: int = port
        self._SSL: bool = SSL
        self._pingWait: int = pingwait
        self._lastPing: float = time.time()
        self._connected: bool = False
        self.isSSL:bool = False
        self._socket: socket.socket | ssl.SSLSocket = self.getNewSocket()
        self.readIO = []
        self.writeIO = []
        self.errorIO = []
        self.onDisconnected: Callable = lambda sender, message: None


    async def connect(self) -> None:
        """ IrcController.connect - Creates new socket & Opens connection to IRC server  
        
            :return: None
            :rtype: None
        """
        try:
            self._socket = self.getNewSocket()
            self.readIO.append(self._socket)
            self.writeIO.append(self._socket)
            self._socket.connect((self._server, self._port))
            self._connected = True
        except socket.error as error:
            self.disconnect()
            raise IrcDisconnectError(f"IrcController.connect error: {error}") from error


    def disconnect(self) -> None:
        """
        IrcController.disconnect - Closes sockets & Disconects from IRC server 
        """
        self.readIO = []
        self.writeIO = []
        self._connected = False
        self._socket.close()

    async def send(self, data: str) -> None:
        """ IrcController.send - sends to server 
            
            :param data: string to be sent to IRC server
            :type data: str

            :return: None
            :rtype: None
        """
        try:
            _reader, writer, _err = select.select(self.readIO,self.writeIO,self.errorIO)
            for sock in writer:
                data = f"{data}\r\n" if not data.endswith("\r\n") else data
                sock.send(data.encode())
        except socket.error as error:
            self.disconnect()
            raise IrcDisconnectError(f"IrcController.send error: {error}") from error

    async def receive(self) -> str | None:
        """ IrcController.receive - Receives all data from socket buffer 
        
            :return: All available data from socket buffer, if none is available returns None
            :rtype: str or None
        """
        buffer = None
        await self._ping()
        try:
            reader, _writer, _err = select.select(self.readIO, self.writeIO, self.errorIO)
            for sock in reader:
                buffer = sock.recv(4096)
                buffer =  buffer.decode()
                if buffer.startswith("PING"):
                    await self._pong()
                return buffer
        except socket.error as error:
            self.disconnect()
            raise IrcDisconnectError(f"IrcController.recieve error: {error}") from error

    def isConnected(self)->bool:
        """ IrcController.isConnected - Gets status of server connection"""
        return self._connected

    async def _ping(self) -> None:
        """ IrcController._ping - sends keep alive ping if pingwait timer runs out  
        
            :return: None
            :rtypr: None
        """
        try:
            if time.time() - self._lastPing > self._pingWait:
                self._lastPing = time.time()
                await self.send("PING")
        except socket.error as error:
            self.disconnect()
            raise IrcDisconnectError(f"IrcController._ping error: {error}")from error

    async def _pong(self) -> None:
        """ IrcController._pong - replies to server ping 

            :return: None
            :rtypr: None   
        """
        try:
            self._lastPing = time.time()
            await self.send("PONG")
        except socket.error as error:
            self.disconnect()
            raise IrcDisconnectError(f"IrcController._pong error: {error}") from error


    def getNewSocket(self) -> socket.socket:
        """
        getNewSocket _summary_

        _extended_summary_

        :return: _description_
        :rtype: socket.socket
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if self._SSL:
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
            context.load_verify_locations(certifi.where())
            context.post_handshake_auth = True
            sock = context.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM), server_hostname=self._server)
            self.isSSL = True
        return sock 
    