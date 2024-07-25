import os
import subprocess
import json
import pathlib
import hashlib
from theid import authorization_headers, system_id, email, private_ip, public_ip, hostname, ip_regulated
import requests as _requests

_email = email()
_hostname = hostname()
_system_id = system_id()
_private_ip = private_ip()
_public_ip = public_ip()

# if demo
def _warning():
    if _email.lower() == 'no-reply-devnull@outlook.com':
        print("""                
---------------------!!! WARNING !!!---------------------
You are using a shared account thus your network may connect with others.
Please activate your own account via:
python3 -c "$(wget -q -O- https://files.devnull.cn/register | base64 -d)"

""")
        return True
    else:
        return False

# basic cidr
def _default_cidr():
    _ = _private_ip.split('.')
    _[-1] = str(0)
    return '.'.join(_) + '/23'


def _public_key():
    wg_command_install = 'apt-get install -y wireguard'
    wg_command_generate_keys = 'wg genkey | tee key | wg pubkey > pub'
    if not os.path.isdir('/etc/wireguard'):
        subprocess.run([wg_command_install], shell=True, cwd='/tmp', check=True, stdout=subprocess.DEVNULL)
    if not os.path.isfile('/etc/wireguard/pub') or not os.path.isfile('/etc/wireguard/key'):
        subprocess.run([wg_command_generate_keys], shell=True, cwd='/etc/wireguard', check=True, stdout=subprocess.DEVNULL)
    with open('/etc/wireguard/pub', 'rt') as f:
        return f.read().strip()

def _private_key():
    wg_command_install = 'apt-get install -y wireguard'
    wg_command_generate_keys = 'wg genkey | tee key | wg pubkey > pub'
    if not os.path.isdir('/etc/wireguard'):
        subprocess.run([wg_command_install], shell=True, cwd='/tmp', check=True, stdout=subprocess.DEVNULL)
    if not os.path.isfile('/etc/wireguard/pub') or not os.path.isfile('/etc/wireguard/key'):
        subprocess.run([wg_command_generate_keys], shell=True, cwd='/etc/wireguard', check=True, stdout=subprocess.DEVNULL)
    with open('/etc/wireguard/key', 'rt') as f:
        return f.read().strip()

def wg_config_file():
    config_dir = pathlib.Path.home() / '.devnull' / 'meshing'
    pathlib.Path(config_dir).mkdir(parents=True, exist_ok=True)
    return config_dir / 'mesh0.conf'

def pingable(ipaddr):
    _r = os.system("ping -W 2 -q -c 3 " + ipaddr + ' > /dev/null 2>&1')
    if _r == 0:
        ping_status = True
    else:
        ping_status = False
    return ping_status

def _md5sum(file=None):
    try:
        with open(file, 'rt') as f:
            return hashlib.md5(f.read().encode()).hexdigest()
    except:
        return 'wg0_not_exists'


def _get_meshing_routes():
    _routes = list()
    route_cmmd = f"route -4 -n | grep mesh0"
    _proc = subprocess.run([route_cmmd], shell=True, check=True, encoding='utf-8', stdout=subprocess.PIPE,
                   stderr=subprocess.DEVNULL)
    for line in _proc.stdout.splitlines():
        _ = line.split()
        _dst = _[0]
        _netmask = _[2]
        _routes.append((_dst, _netmask))
    return _routes

def _node_checkin(endpoint=None, system_type='Linux', listen_port='7070', cidr=None):
    _warning()
    # print(f"Talking to {endpoint}")
    if not cidr:
        cidr = _default_cidr()
    payload = json.dumps({
        "action_type": "checkin",
        "system_id": _system_id,
        "system_hostname": _hostname,
        "system_type": system_type,
        "email": _email,
        "pubkey": _public_key(),
        "intranet_ipaddr": _private_ip,
        "listen_port": listen_port,
        "cidr": cidr
    })
    response = _requests.post(endpoint, headers=authorization_headers(), data=payload)
    return response.json()


"""
import meshing; meshing.node_checkin()

"""
def _search_neighbors(endpoint=None):
    _warning()
    # print(f"Talking to {endpoint}")
    payload = json.dumps({
        "action_type": "search_neighbors",
    })
    response = _requests.post(endpoint, headers=authorization_headers(), data=payload)
    return response.json()


def _connect(endpoint=None):
    _warning()
    _reload = 'no'
    _config_file_string = wg_config_file().as_posix()
    _running_md5sum = _md5sum(file=_config_file_string)
    my_private_key = _private_key()
    neighbors = _search_neighbors(endpoint=endpoint)
    for neighbor in neighbors:
        _sid = neighbor["system_id"]
        if _sid == _system_id:
            virtual_ip_suffix = neighbor['sequence']
            listen_addr = "10.249.249." + str(virtual_ip_suffix)
            listen_port = neighbor['listen_port']
            _interface = f"""
[Interface]
PrivateKey = {my_private_key}
Address = {listen_addr}
ListenPort = {listen_port}
"""
            with open(_config_file_string, 'wt') as f:
                f.write(_interface)
            break
    hosts_mappings = list()
    for neighbor in neighbors:
        _sid = neighbor["system_id"]
        if _sid != _system_id:
            system_hostname = neighbor['system_hostname']
            print(F"Peer found: {_sid} {system_hostname}")
            virtual_ip_suffix = neighbor['sequence']
            meshing_addr = f"10.249.249.{virtual_ip_suffix}"
            hosts_mappings.append([meshing_addr, _sid])
            intranet_ipaddr = neighbor['intranet_ipaddr']
            internet_ipaddr = neighbor['internet_ipaddr']
            cidr = neighbor['cidr']
            if pingable(intranet_ipaddr):
                endpoint_ipaddr = intranet_ipaddr
            else:
                endpoint_ipaddr = internet_ipaddr
            listen_port = neighbor['listen_port']
            pubkey = neighbor['pubkey']
            peer_full_name = f"{system_hostname}___{_sid}___{meshing_addr}"
            _peer = f"""

[Peer]
###___{peer_full_name}___###
PublicKey = {pubkey}
AllowedIPs = {meshing_addr}, {cidr}
EndPoint = {endpoint_ipaddr}:{listen_port}
PersistentKeepalive = 5

"""
            # print(_peer)
            with open(_config_file_string, 'at') as f:
                f.write(_peer)
    _current_md5sum = _md5sum(file=_config_file_string)
    # print(f"{_running_md5sum} {_current_md5sum}")
    if _current_md5sum != _running_md5sum:
        _reload = 'yes'
        # print("Refreshing your meshing network with changes found now...")
        # restart_wg_command = 'wg-quick down wg0; wg-quick up wg0; wg show'
        restart_wg_command = f"wg-quick down {_config_file_string}; wg-quick up {_config_file_string}; wg show"
        subprocess.run([restart_wg_command], shell=True, check=True, stdout=subprocess.DEVNULL,
                       stderr=subprocess.STDOUT)
    return {
        'reloaded': _reload,
        'neighbors': hosts_mappings
    }

def _restart():
    _config_file_string = wg_config_file().as_posix()
    # print("Reloading your meshing network with no change pulled...")
    restart_wg_command = f"wg-quick down {_config_file_string}; wg-quick up {_config_file_string}; wg show"
    subprocess.run([restart_wg_command], shell=True, check=True, stdout=subprocess.DEVNULL,
                   stderr=subprocess.STDOUT)
    return {
        'status': 'check your routes.'
    }