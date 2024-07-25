from ._utils import _public_key
from ._utils import _node_checkin, _search_neighbors, _connect, _restart

def public_key():
    return _public_key()

def checkin(endpoint="https://devnull.cn/meshing",listen_port=7070, cidr=None):
   return _node_checkin(endpoint=endpoint,listen_port=listen_port, cidr=cidr)

def neighbors(endpoint="https://devnull.cn/meshing"):
    return _search_neighbors(endpoint=endpoint)

def connect(endpoint="https://devnull.cn/meshing"):
    return _connect(endpoint=endpoint)

def restart():
    return _restart()
