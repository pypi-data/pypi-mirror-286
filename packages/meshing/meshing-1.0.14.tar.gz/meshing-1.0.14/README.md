# meshing-sdk-python
Python SDK to run a WireGuard mesh network.

```bash
echo 'y' | pip3 uninstall meshing
pip3 install meshing --no-cache-dir

# development test with KVM VMs
python3 -c 'import meshing; meshing.checkin(endpoint="http://192.168.101.1:8000/webapps")'
python3 -c 'import meshing; meshing.neighbors(endpoint="http://192.168.101.1:8000/webapps")'
python3 -c 'import meshing; meshing.connect(endpoint="http://192.168.101.1:8000/webapps")'
python3 -c 'import meshing; meshing.restart()'

# test in cloud
python3 -c 'import meshing; meshing.checkin()'
python3 -c 'import meshing; meshing.neighbors()'
python3 -c 'import meshing; meshing.connect()'
python3 -c 'import meshing; meshing.restart()'
```

```python
import meshing
meshing.checkin()

```

