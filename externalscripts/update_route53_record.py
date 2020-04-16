#!/usr/bin/env python

import argparse
import sys

import boto3


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update Route53 with Zabbix Pod IP")
    parser.add_argument("-i", "--podip", required=True, help="pod ip")
    args = parser.parse_args()

    if not args.podip:
        sys.exit("ERROR: podip is empty")

    route53 = boto3.client("route53")

    response = route53.change_resource_record_sets(
        HostedZoneId="Z035919975LWHPRRJ4IY",
        ChangeBatch={
            "Comment": "updating zabbix pod ip",
            "Changes": [
                {
                    "Action": "UPSERT",
                    "ResourceRecordSet": {
                        "Name": "zabbix.austin.local.",
                        "Type": "A",
                        "TTL": 300,
                        "ResourceRecords": [{"Value": args.podip},],
                    },
                },
            ],
        },
    )
    print("Successfully updated route53. May take a few minutes to propagate.")
