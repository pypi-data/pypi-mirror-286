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


def _node_checkin(system_type='Linux', listen_port='7000'):
    url = "https://devnull.cn/meshing"
    payload = json.dumps({
        "action_type": "checkin",
        "system_id": _system_id,
        "system_hostname": _hostname,
        "system_type": system_type,
        "email": _email,
        "pubkey": _public_key(),
        "intranet_ipaddr": _private_ip,
        "listen_port": listen_port
    })
    # print("Payload:", payload)
    response = _requests.post(url, headers=authorization_headers(), data=payload)
    return response.json()


"""
import meshing; meshing.node_checkin()

"""
def _search_neighbors():
    url = "https://devnull.cn/meshing"
    payload = json.dumps({
        "action_type": "search_neighbors",
    })
    response = _requests.post(url, headers=authorization_headers(), data=payload)
    return response.json()


def _connect():
    _reload = 'no'
    config_dir = pathlib.Path.home() / '.devnull' / 'meshing'
    pathlib.Path(config_dir).mkdir(parents=True, exist_ok=True)
    wg_config_file = config_dir / 'mesh0.conf'
    _running_md5sum = _md5sum(wg_config_file)
    # wg_config_file = '/etc/wireguard/mesh0.conf'
    my_private_key = _private_key()
    neighbors = _search_neighbors()
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
            with open(wg_config_file, 'wt') as f:
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
AllowedIPs = {meshing_addr}
EndPoint = {endpoint_ipaddr}:{listen_port}

"""
            # print(_peer)
            with open(wg_config_file, 'at') as f:
                f.write(_peer)
    _current_md5sum = _md5sum(wg_config_file)
    if _current_md5sum != _running_md5sum:
        _reload = 'yes'
        print("meshing network information changed, reloading ...")
        # restart_wg_command = 'wg-quick down wg0; wg-quick up wg0; wg show'
        restart_wg_command = f"wg-quick down {wg_config_file}; wg-quick up {wg_config_file}; wg show"
        subprocess.run([restart_wg_command], shell=True, check=True, stdout=subprocess.DEVNULL,
                       stderr=subprocess.STDOUT)
    return {
        'reloaded': _reload,
        'neighbors': hosts_mappings
    }
