import socket
from urllib.request import urlopen

from xml.etree.ElementTree import parse

msg = \
    'M-SEARCH * HTTP/1.1\r\n' \
    'HOST:239.255.255.250:1900\r\n' \
    'ST:upnp:rootdevice\r\n' \
    'MX:2\r\n' \
    'MAN:"ssdp:discover"\r\n' \
    '\r\n'
import xmltodict

# Set up UDP socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
s.settimeout(2)
s.sendto(msg.encode(), ('239.255.255.250', 1900) )

try:
    while True:
        data, addr = s.recvfrom(65507)

        print(addr[0])
        if "Philips" in data.decode("utf-8"):
            print("True")
            file = urlopen('http://'+addr[0]+'/description.xml')
            data = file.read()
            file.close()

            data = xmltodict.parse(data)
            xom=data["root"]
            print(((data["root"])["device"])["friendlyName"])
        else:
            print("false")
except socket.timeout:
    pass
