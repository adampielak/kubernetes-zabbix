#!/usr/bin/env python

import argparse
import sys

from zabbix.api import ZabbixAPI
from get_zabbix_secrets import get_secret

ZABBIX_USER, ZABBIX_PASSWORD = get_secret()

ZABBIX_SERVER = "http://zabbix-web-nginx-pgsql-clusterip"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Delete host from Zabbix server")
    parser.add_argument("-n", "--hostname", required=True, help="Zabbix hostname")
    args = parser.parse_args()

    zapi = ZabbixAPI(url=ZABBIX_SERVER, user=ZABBIX_USER, password=ZABBIX_PASSWORD)

    """Get hostid by hostname"""
    result = zapi.do_request(
        "host.get", {"filter": {"host": [args.hostname]}, "output": ["name", "hostid"]}
    )

    if not result["result"]:
        sys.exit("hostname not found")

    """Delete host from Zabbix server"""
    hostid = result["result"][0]["hostid"]
    result = zapi.do_request("host.delete", [hostid])
    print(result)
