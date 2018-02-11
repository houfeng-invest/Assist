import socket
import os
import sys

services = {'ftp':21,'ssh':22,'smtp':25,'http':80,'https':443}
def retBanner(ip,port):
    try:
        socket.setdefaulttimeout(2)
        s = socket.socket()
        s.connect((ip,port))
        banner = s.recv(1024)
        print("ip:{0}:{1} {2}".format(ip,port,banner))
        return banner
    except Exception as e:
        # print("ip:{0}:{1} {2}".format(ip,port,e))
        return

def checkVulns(banner):
    pass
def main():
    ip1 = '192.168.1.137'
    portList = [21,22,25,80,110,443]
    for x in range(1,255):
        ip = '192.168.1.'+str(x)
        for port in portList:
            banner = retBanner(ip,port)




if __name__ == '__main__':
    main()
