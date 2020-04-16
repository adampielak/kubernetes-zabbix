#!/usr/bin/env python

import argparse
import sys

from zabbix.api import ZabbixAPI
from get_zabbix_secrets import get_secret

ZABBIX_USER, ZABBIX_PASSWORD = get_secret()

ZABBIX_SERVER = "http://zabbix-web-nginx-pgsql-clusterip"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Register internal ip to Zabbix host-macro"
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
        sys.exit(0)
    hostid = result["result"][0]["hostid"]

    """get hostmacroid of macro we're changing"""
    hostmacroid = None
    result = zapi.do_request("usermacro.get", {"hostids": hostid})
    for i in result["result"]:
        if i["macro"] == "{$NGINX_HOST}":
            hostmacroid = i["hostmacroid"]
            break

    """if macro is not a user macro yet, initialize it"""
    if hostmacroid == None:
        result = zapi.do_request(
            "usermacro.create",
            {"hostid": hostid, "macro": "{$NGINX_HOST}", "value": args.internalip},
        )
        quit()

    """Update internal ip macro"""
    result = zapi.do_request(
        "usermacro.update", {"hostmacroid": hostmacroid, "value": args.internalip}
    )
    print(result["result"])
