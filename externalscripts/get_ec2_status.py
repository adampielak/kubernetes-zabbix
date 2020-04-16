#!/usr/bin/env python

import argparse
import sys

import boto3


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get EC2 instance status from AWS")
    parser.add_argument("-r", "--region", required=True, help="AWS region name")
    parser.add_argument("-i", "--instanceid", required=True, help="EC2 instance-id")
    args = parser.parse_args()

    if not args.region:
        sys.exit("ERROR: region is empty")
    if not args.instanceid:
        sys.exit("ERROR: instanceid is empty")
    if args.instanceid == "unknown":
        sys.exit("unknown")
    if args.instanceid[0:2] != "i-":
        sys.exit("ERROR: invalid instanceid")

    ec2 = boto3.client("ec2", args.region)

    instances = ec2.describe_instances(InstanceIds=[args.instanceid])

    state = None
    for reservations in instances["Reservations"]:
        for instance in reservations["Instances"]:
            state = instance["State"]["Name"]

    if not state:
        sys.exit("not found")

    print(state)
