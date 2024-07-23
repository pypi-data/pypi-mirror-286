import json
import socket
import hashlib
import requests
import time
from theid import hostname, system_id, public_ip, private_ip, authorization_headers

bufferSize = 256
# _hostname = hostname()
# _system_id = system_id()
# _private_ip = private_ip()
# _public_ip = public_ip()


def _ingress_check(protocol='udp', port='7000', dev_mode=False):
    _hostname = hostname()
    _system_id = system_id()
    _private_ip = private_ip()
    _public_ip = public_ip()
    send_data_json = {
        "hostname": _hostname,
        "system_id": _system_id,
        "private_ip": _private_ip,
        "public_ip": _public_ip,
    }
    ingress_status = 'unhealthy'
    port = int(port)
    _authorization_headers = authorization_headers()
    if dev_mode is True:
        _private_ip = '127.0.0.1'
        remote_check_url = "http://127.0.0.1:8000/api/centralized-api"
        send_data_json['dev_mode'] = True
        send_data_json['private_ip'] = _private_ip
    else:
        remote_check_url = "https://devnull.cn/ingress"
    if protocol.lower() == 'udp':
        protocol = 'udp'
        _server = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    else:
        protocol = 'tcp'
        _server = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    send_data_json['protocol'] = protocol
    send_data_json['port'] = port
    expected_sha256 = hashlib.sha256(
        (_hostname + _system_id + _private_ip + _public_ip + protocol + str(port)).encode()).hexdigest()
    print("Expected SHA256: {}".format(expected_sha256))
    _server.bind((_private_ip, port))
    time_start = time.time()
    _timeout = 5
    while time.time() - time_start < _timeout:
        print(f"Talking to API: {remote_check_url}")
        # print(f"Sending data: {send_data_json}\n")
        _r = requests.post(remote_check_url, data=json.dumps(send_data_json), headers=_authorization_headers)
        print(f"API response: {_r.json()}")
        time.sleep(1)
        _received = _server.recvfrom(bufferSize)
        print(_received)
        _received_sha256 = _received[0]
        if _received_sha256.decode() == expected_sha256:
            ingress_status = 'healthy'
        return {
            'ingress_status': ingress_status,
            'protocol': protocol,
            'port': port
        }

