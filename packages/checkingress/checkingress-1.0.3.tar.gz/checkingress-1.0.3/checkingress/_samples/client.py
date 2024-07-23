import socket
import json
import hashlib

remote_port = 7000
msgFromClient = "Hello UDP Server"
bytesToSend = str.encode(msgFromClient)
serverAddressPort = ("127.0.0.1", int(remote_port))
bufferSize = 1024

received_data_json =  {
    '_hostname': 'orchard',
    '_system_id': 'e64ab96324ef1899498889a0e3eabcb4',
    '_private_ip': '192.168.1.6',
    '_public_ip': '115.171.233.106',
    '_port': 7000
}

_hostname= received_data_json['_hostname']
_system_id = received_data_json['_system_id']
_private_ip = received_data_json['_private_ip']
_public_ip = received_data_json['_public_ip']
_port = received_data_json['_port']

sending_string = hashlib.sha256((_hostname + _system_id + _private_ip + _public_ip + str(_port)).encode()).hexdigest()
# Create a UDP socket at client side
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Send to server using created UDP socket
# UDPClientSocket.sendto(bytesToSend, serverAddressPort)

bytesToSend = str.encode(sending_string)
UDPClientSocket.sendto(bytesToSend, serverAddressPort)

msgFromServer = UDPClientSocket.recvfrom(bufferSize)
msg = "Message from Server {}".format(msgFromServer[0])
print(msg)