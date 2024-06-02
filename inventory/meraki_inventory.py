#!/usr/bin/env python
"""
meraki_inventory.py - Generates an Ansible dynamic inventory using NMAP
Author
Steven Carter (stevenca@cisco.com)
"""
import meraki
import boto3
import json
import os
import logging
import requests
import re
import pprint
from botocore.exceptions import ClientError


type_by_platform = {
    "MX": "appliance",
    "VMX": "appliance",
    "MR": "wireless",
    "MS": "switch",
    "MG": "cellularGateway",
    "MT": "sensor",
    "CW": "wireless",
    "Z": "appliance",
}

def get_secret(secret_name):
    region_name = "us-east-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    return (json.loads(get_secret_value_response['SecretString']))

def get_device_type(model):
    for platform in type_by_platform:
        if device["model"].startswith(platform):
            device_type = type_by_platform[platform]
            return (platform, device_type)
    return ("unkown", "unkown")

def add_to_group(group, item):
    if group in groups:
        groups[group].append(item)
    else:
        groups[group] = [item]

def get_org_radius_servers(organizationId, meraki_api_key):
    url = f"https://api.meraki.com/api/v1/organizations/{organizationId}/auth/radius/servers"
    headers = {
        "Authorization": "Bearer " + meraki_api_key,
        "Accept": "application/json"
    }
    response = requests.request('GET', url, headers=headers, data = None)
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return None

if __name__ == "__main__":

    # meraki_secrets = get_secret('meraki/cpn')
    meraki_api_key = os.environ.get('MERAKI_DASHBOARD_API_KEY')
    meraki_base_url = os.environ.get('MERAKI_BASE_URL')
    meraki_org_id = os.environ.get('MERAKI_ORG_ID')
    dashboard = meraki.DashboardAPI(api_key=meraki_api_key,
                                            base_url=meraki_base_url,
                                            output_log=False,
                                            log_file_prefix=os.path.basename(__file__)[:-3],
                                            log_path='',
                                            print_console=False)

    # devices = get_org_devices(meraki_secrets['MERAKI_ORG_ID'])

    hostvars = {}
    ungrouped = []
    groups = {}
    network_by_id = {}
    meraki_org_id = os.environ.get('MERAKI_ORG_ID')

    meraki_networks = dashboard.organizations.getOrganizationNetworks(
        meraki_org_id, total_pages='all'
    )
    org_radius_servers = get_org_radius_servers(meraki_org_id, meraki_api_key)
    for network in meraki_networks:
        network_by_id[network["id"]] = network
        meraki_devices = dashboard.networks.getNetworkDevices(
            network["id"]
        )
        # Treat the network as a devices since it is a single unit that can be configured
        # network_device_name = "network_" + network["name"]
        network_device_name = network["name"]
        hostvars[network_device_name] = network
        # Add the network ID to the same variable it is in for the devices
        hostvars[network_device_name]["networkId"] = network["id"]
        hostvars[network_device_name]["device_platform"] = "network"

        # Add a meraki tag so we know what type of device this is
        hostvars[network_device_name]["tags"].append("meraki")        

        # Group by Network
        add_to_group(network["name"], network_device_name)
        add_to_group("network", network_device_name)
        add_to_group("meraki", network_device_name)

        # Group by Type
        for product_type in network["productTypes"]:
            add_to_group(product_type, network_device_name)

        # Iterate through devices
        for device in meraki_devices:
            if device["name"]:
                device_name = device["name"]
            else:
                device_name = device["serial"]

            # Add to hostvars
            hostvars[device_name] = device

            if "lanIp" in device:
                primary_ip = device["lanIp"]
            elif "wan1Ip" in device:
                primary_ip = device["wan1Ip"]
            else:
                primary_ip = None
            hostvars[device_name]["primary_ip"] = primary_ip

            # Group by Platform
            device_platform, device_type = get_device_type(device["model"])
            hostvars[device_name]["device_type"] = device_type
            hostvars[device_name]["device_platform"] = device_platform
            add_to_group(device_platform, device_name)
            add_to_group(device_type, device_name)

            # Group by Network
            add_to_group(network["name"], device_name)

            # Group by Model
            add_to_group(device["model"], device_name)

            # Add the MX "W"s and "Z"s to the wireless group
            if device["model"].endswith("W"):
                add_to_group("wireless", device_name)

            # Group by Tag
            # Each device gets it's tags plus the network's tags
            device_tags = device["tags"] + network_by_id[device["networkId"]]["tags"]
            for tag in device_tags:
                add_to_group(tag, device_name)

    data = {
        "_meta": {
           "hostvars": hostvars
        },
        "all": {
            "children": [
                # "ungrouped"
            ],
            "vars": {
                "meraki_api_key": meraki_api_key,
                "meraki_base_url": meraki_base_url,
                "meraki_org_id": meraki_org_id,
                "orgId": meraki_org_id,
                "org_radius_servers": org_radius_servers,
            }
        }
    }

    group_name_re = re.compile('[^A-Za-z0-9_]')
    # Add Network Groups
    for item in groups:
        group_name = group_name_re.sub('_', item) 
        data["all"]["children"].append(group_name)
        data[group_name] = {
                "hosts": groups[item]
        }

    print(json.dumps(data, indent=4))

