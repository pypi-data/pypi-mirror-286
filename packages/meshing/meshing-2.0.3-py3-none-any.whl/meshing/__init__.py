from ._utils import _public_key, _connect
from ._utils import _node_checkin, _search_neighbors
from ._utils import _restart, _get_meshing_routes

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
def routes():
    return _get_meshing_routes()

