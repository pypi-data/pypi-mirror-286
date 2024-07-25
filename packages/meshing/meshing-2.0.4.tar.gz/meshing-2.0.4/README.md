# meshing-sdk-python

#### Build your meshing network in seconds.

```bash
## Prerequisites: 
# 1, At least 1 instance with public ip allows UDP inbound. By default, it is udp/7070.
# 2, Permission to update your routing tables in your VPC.

# 1st, Run following in every instance:
python3 -c 'import meshing; meshing.checkin()'

# 2nd, Make sure above checkin() completed in ALL regions, then connect():
python3 -c 'import meshing; meshing.connect()'

# 3rd, check your interface, and you can ping each other by now.
ifconfig mesh0

# 4th, if you need connecting the subnets behind, update routes in VPC or home router.
# This parts vary depending your specific requirements.

# 5th, if your need update the default local cidr in routing:
# by default your_local_ipaddr_by_/23 is used.
python3 -c 'import meshing; meshing.checkin(cidr="1.2.3.0/24")' # or
python3 -c 'import meshing; meshing.checkin(cidr="1.2.3.0/24, 2.3.4.0/24")' # one-string-by-comma
python3 -c 'import meshing; meshing.connect()' # connect() again in all regions.


# Good Luck.
```
