#!/usr/bin/env python

import argparse
import sys

from zabbix.api import ZabbixAPI
from get_zabbix_secrets import get_secret

ZABBIX_USER, ZABBIX_PASSWORD = get_secret()

ZABBIX_SERVER = "http://zabbix-web-nginx-pgsql-clusterip"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Register private ip to host interface"
    )
    parser.add_argument("-n", "--hostname", required=True, help="Zabbix hostname")
    parser.add_argument("-i", "--internalip", required=True, help="internal ip")
    args = parser.parse_args()

    if not args.hostname:
        sys.exit("ERROR: hostname is empty")
    if not args.internalip:
        sys.exit("ERROR: internal ip is empty")
    if args.internalip == "unknown":
        sys.exit("unknown")

    """login to zabbix and get hostid"""
    zapi = ZabbixAPI(url=ZABBIX_SERVER, user=ZABBIX_USER, password=ZABBIX_PASSWORD)
    result = zapi.do_request(
        "host.get", {"filter": {"host": [args.hostname]}, "output": ["name", "hostid"]}
    )
    if not result["result"]:
        sys.exit("Hostname not found")
    hostid = result["result"][0]["hostid"]

    """use hostid to get interfaceid"""
    result = zapi.do_request(
        "hostinterface.get", {"filter": {"hostid": hostid}, "output": ["interfaceid"]}
    )
    interfaceid = result["result"][0]["interfaceid"]

    """update interface"""
    result = zapi.do_request(
        "hostinterface.update", {"interfaceid": interfaceid, "ip": args.internalip}
    )
    print(result["result"])
