import os
import subprocess
import json
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
