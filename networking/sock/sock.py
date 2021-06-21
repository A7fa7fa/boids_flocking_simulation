import socket
import json
from uuid import uuid4
from networking.sock.address import __initserverhost

import threading


# the first ´BYTE_COUNT´ of msg recieved or send are the length of msg
BYTE_COUNT = 4

# local IPV4 Adress
SERVER = socket.gethostbyname(socket.gethostname())
# external IPV4 Adress
#SERVER = __initserverhost()

PORT = 5051

# on this addr socket will listen create connections from
ADDR = (SERVER, PORT)

# decrypt/encrypt msg in this format
FORMAT = 'utf-8'

class MySocket:
    """my first try of a socket class
    probaly not very efficient and there are better ways to do it
    but it works
    """


    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        else:
            self.sock = sock


    def connect(self, addr):
        try:
            self.sock.connect(addr)
            return True
        except Exception as e:
            print(e)
            return False


    def send_msg(self, msg):
        """Send a message via the socket."""

        # add header msg_length to msg before sending
        msg = self.add_msg_header(self.encode_msg(msg))
        self.sock.sendall(msg)


    def recv_msg(self) -> str:
        """Receive a message via the socket."""
        
        # start by getting the header (which is an int of length `BYTE_COUNT`). 
        # The header tells the message size in bytes.
        raw_msglen = self.recvall(BYTE_COUNT)

        if not raw_msglen:
            return None
        # Then retrieve a message of length `raw_msglen`
        # this will be the actual message
        msglen = self.decode_msg(raw_msglen)
        if not msglen:
            return None
        return self.decode_msg(self.recvall(msglen))


    def recvall(self, length) -> bytearray:
        """Get a message of a certain length from the socket stream"""

        data = bytearray()
        while len(data) < int(length): # check if still connected or in try/expet
            try:
                packet = self.sock.recv(int(length) - len(data))
                if not packet:
                    return None
                data.extend(packet)
            except Exception as e:
                print(e)
                return None    

        return data


    def len_inbytes(self, msg) -> bytes:
        """returns length of bytearray ´bmsg´ as byte"""

        return self.encode_msg(len(msg))
        #return len(msg).to_bytes(BYTE_COUNT, byteorder='big')


    def len_frombytes(self, bmsg) -> int:
        """returns length of bytearray ´bmsg´ as integer"""
        try:
            return int.from_bytes(bmsg, byteorder='big')
        except Exception as e:
            print(e)
            return None

    def add_msg_header(self, msg:bytes) -> bytes:
        """add header to msg. header tells the msg size in bytes """

        return self.len_inbytes(msg) + msg


    def encode_msg(self, msg:str) -> bytes:
        """convert the str ´msg´ to bytes"""

        return json.dumps(msg).encode(encoding=FORMAT,errors='strict')


    def decode_msg(self, msg:bytes) -> str:
        """convert the bytes ´msg´ to str"""

        return msg.decode(encoding=FORMAT,errors='strict')
