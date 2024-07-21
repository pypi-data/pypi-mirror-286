import asyncio
import socket
import ssl
import time
import certifi

class IrcDisconnectError(Exception):
    pass

class IrcController():
    """ IRC Conroller

        :param server: address to IRC server
        :type server: str

        :param port: IRC server port
        :type port: int

        :param pingwait: keep alive delay 
        :type ping: int
    """
    def __init__(self, server: str, port: int, SSL:bool = False, pingwait: int = 300)->None:
        # Populate values
        self._server: str = server
        self._port: int = port
        self._SSL:bool = SSL
        self._pingWait: int = pingwait
        self._lastPing: time = time.time()
        self._connected: bool = False
        self.isSSL:bool = False
        self._socket: socket.socket | ssl.SSLSocket = None
        
    async def connect(self)->None:
        """ IrcController.connect - Creates new socket & Opens connection to IRC server  
        
            :return: None
            :rtype: None
        """
        try:
            # Create new socket and connect
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            if self._SSL:
                context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
                context.load_verify_locations(certifi.where())
                context.post_handshake_auth = True
                self._socket = context.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM), server_hostname=self._server)
                self.isSSL = True
            self._socket.connect((self._server, self._port))
            self._connected = True

        except socket.error as error:
            self.disconnect()
            raise IrcDisconnectError(f"IRC error: {error}")
           
            
    def disconnect(self)->None:
        """
        IrcController.disconnect - Closes sockets & Disconects from IRC server 
        """
        self._connected = False
        self._socket.close()
        

    async def send(self, data: str)->None:
        """ IrcController.send - sends to server 
            
            :param data: string to be sent to IRC server
            :type data: str

            :return: None
            :rtype: None
        """

        try:
            data = f"{data}\r\n" if not data.endswith("\r\n") else data
            self._socket.send(data.encode())
        except socket.error as error:
            await self.disconnect()
            raise IrcDisconnectError(f"IRC error: {error}")

    async def receive(self)->str:
        """ IrcController.receive - Receives all data from socket buffer 
        
            :return: All available data from socket buffer, if none is available returns None
            :rtype: str or None
        """
        buffer = None
        await self._ping()
        try:
            # Should be ready to read
            buffer = self._socket.recv(4096)
            data = buffer.decode()
            if data.startswith("PING"):
                self._pong(data)
            return data
        except socket.error as error:
            self.disconnect()
            raise IrcDisconnectError(f"IRC error: {error}")
        
    def isConnected(self)->bool:
        """ IrcController.isConnected - Gets status of server connection
            
            :return: self._connected
            :rtype: bool
        """
        return self._connected

    async def _ping(self)->None:
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
            raise IrcDisconnectError(f"IRC error: {error}")
            

    async def _pong(self, data: str)->None:
        """ IrcController._pong - replies to server ping 

            :return: None
            :rtypr: None   
        """
        try:
            self._lastPing = time.time()
            await self.send(data.replace("PING", "PONG"))
        except socket.error as error:
            self.disconnect()
            raise IrcDisconnectError(f"IRC error: {error}")