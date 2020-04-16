#!/usr/bin/env python

import argparse
import sys

from zabbix.api import ZabbixAPI
from get_zabbix_secrets import get_secret

ZABBIX_USER, ZABBIX_PASSWORD = get_secret()

ZABBIX_SERVER = "http://zabbix-web-nginx-pgsql-clusterip"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Register instance-id to Zabbix host-macro"
    )
    parser.add_argument("-n", "--hostname", required=True, help="Zabbix hostname")
    parser.add_argument("-i", "--instanceid", required=True, help="EC2 instance-id")
    args = parser.parse_args()

    if not args.hostname:
        sys.exit("ERROR: hostname is empty")
    if not args.instanceid:
        sys.exit("ERROR: instanceid is empty")
    if args.instanceid == "unknown":
        sys.exit("unknown")
    if args.instanceid[0:2] != "i-":
        sys.exit("ERROR: invalid instanceid")

    """login to zabbix and get hostid"""
    zapi = ZabbixAPI(url=ZABBIX_SERVER, user=ZABBIX_USER, password=ZABBIX_PASSWORD)
    result = zapi.do_request(
        "host.get", {"filter": {"host": [args.hostname]}, "output": ["name", "hostid"]}
    )
    if not result["result"]:
        sys.exit("Hostname not found")
    hostid = result["result"][0]["hostid"]

    """Write instance ID to host macro"""
    result = zapi.do_request(
        "usermacro.create",
        {"hostid": hostid, "macro": "{$EC2_INSTANCEID}", "value": args.instanceid},
    )
    print(result["result"])
