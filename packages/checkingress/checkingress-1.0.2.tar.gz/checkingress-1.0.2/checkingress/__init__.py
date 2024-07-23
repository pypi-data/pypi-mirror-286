from ._server import _ingress_check

def check(protocol="udp", port="7000", dev_mode=False):
    return _ingress_check(protocol=protocol, port=port, dev_mode=dev_mode)
