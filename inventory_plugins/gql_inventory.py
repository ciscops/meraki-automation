from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
name: gql_inventory
author:
  - Network to Code (@networktocode)
  - Armen Martirosyan (@armartirosyan)
short_description: Nautobot inventory source using GraphQL capability
description:
  - Get inventory hosts from Nautobot using GraphQL queries
extends_documentation_fragment:
  - constructed
  - inventory_cache
requirements:
  - netutils
options:
  plugin:
    description: Setting that ensures this is a source file for the 'networktocode.nautobot' plugin.
    required: True
    choices: ["gql_inventory"]
  api_endpoint:
    description: Endpoint of the Nautobot API
    required: True
    env:
      - name: NAUTOBOT_URL
  timeout:
    description: Timeout for Nautobot requests in seconds
    type: int
    default: 60
  follow_redirects:
    description:
      - Determine how redirects are followed.
      - By default, I(follow_redirects) is set to uses urllib2 default behavior.
    default: urllib2
    choices: ["urllib2", "all", "yes", "safe", "none"]
  validate_certs:
    description:
      - Allows connection when SSL certificates are not valid. Set to C(false) when certificates are not trusted.
    default: True
    type: boolean
  token:
    required: True
    description:
      - Nautobot API token to be able to read against Nautobot.
      - This may not be required depending on the Nautobot setup.
    env:
      # in order of precedence
      - name: NAUTOBOT_TOKEN
  query:
    required: False
    description:
      - GraphQL query parameters or filters to send to Nautobot to obtain desired data
    type: dict
    default: {}
    suboptions:
      devices:
        description:
          - Additional query parameters or filters for devices
        type: dict
        required: false
      virtual_machines:
        description:
          - Additional query parameters or filters for VMs
        type: dict
        required: false
  group_by:
    required: False
    description:
      - List of dot-sparated paths to index graphql query results (e.g. `platform.display`)
      - The final value returned by each path is used to derive group names and then group the devices into these groups.
      - Valid group names must be string, so indexing the dotted path should return a string (i.e. `platform.display` instead of `platform`)
      - > 
          If value returned by the defined path is a dictionary, an attempt will first be made to access the `name` field, and then the `display` field.
          (i.e. `platform` would attempt to lookup `platform.name`, and if that data was not returned, it would then try `platform.display`)
    type: list
    elements: str
    default: []
  group_names_raw:
      description: Will not add the group_by choice name to the group names
      default: False
      type: boolean
      version_added: "4.6.0"
"""

import json
import os
from sys import version as python_version
from ansible.plugins.inventory import BaseInventoryPlugin, Constructable, Cacheable
from ansible.module_utils.ansible_release import __version__ as ansible_version
from ansible.errors import AnsibleError, AnsibleParserError
from ansible.module_utils.urls import open_url

from ansible.module_utils.six.moves.urllib import error as urllib_error
from ansible.module_utils.common.text.converters import to_native

body = """ 
{
  device_list {
    name
    interfaces {
      name
      description
      enabled
      tags {
        id
      }
      tagged_vlans {
        vid
      }
      untagged_vlan {
        vid
      }
      mode
      ip_addresses {
        display
      }
    }
  }
}
"""

class InventoryModule(BaseInventoryPlugin, Constructable, Cacheable):
    NAME = "gql_inventory"

    def verify_file(self, path):
        # """Return true/false if this is possibly a valid file for this plugin to consume."""
        # if super(InventoryModule, self).verify_file(path):
        #     # Base class verifies that file exists and is readable by current user
        #     if path.endswith((".yml", ".yaml")):
        #         return True

        # return False
        return True

    def main(self):
        try:
            self.display.vvvv(f"JSON query: {body}")
            response = open_url(
                self.api_endpoint + "/graphql/",
                method="post",
                data=json.loads(body),
                headers=self.headers,
                timeout=self.timeout,
                validate_certs=self.validate_certs,
                follow_redirects=self.follow_redirects,
            )
        except urllib_error.HTTPError as err:
            raise AnsibleParserError(to_native(err.fp.read()))
        json_data = json.loads(response.read())
        self.display.vvvv(f"JSON response: {json_data}")

    def parse(self, inventory, loader, path, cache=True):
        super(InventoryModule, self).parse(inventory, loader, path)
        self._read_config_data(path=path)
        self.use_cache = cache

        # Nautobot access
        token = self.get_option("token")
        # Handle extra "/" from api_endpoint configuration and trim if necessary, see PR#49943
        self.api_endpoint = self.get_option("api_endpoint").strip("/")
        self.validate_certs = self.get_option("validate_certs")
        self.timeout = self.get_option("timeout")
        self.headers = {
            "User-Agent": "ansible %s Python %s" % (ansible_version, python_version.split(" ", maxsplit=1)[0]),
            "Content-type": "application/json",
        }
        if token:
            self.headers.update({"Authorization": "Token %s" % token})

        self.gql_query = self.get_option("query")
        self.group_by = self.get_option("group_by")
        self.follow_redirects = self.get_option("follow_redirects")
        self.group_names_raw = self.get_option("group_names_raw")

        self.main()

        # Make GraphQL call to fetch inventory data
        # try:
        #     response = requests.post(self.graphql_url, headers=self.headers, json={})
        #     response.raise_for_status()  # Raise error for non-2xx status codes
        #     inventory_data = response.json()
        # except requests.exceptions.RequestException as e:
        #     raise Exception(f"Error fetching inventory data: {e}")

        # Populate inventory object with fetched data
        # Example: inventory.add_host(hostname="example.com", group="example_group")

    # def parse_extra_vars(self, extra_vars):
        # Implement logic to process extra variables
        # Modify inventory data based on extra variables

    # def parse_limit(self, limit):
        # Implement logic to apply limits to inventory
        # Filter inventory data based on the provided limit

# Required for Ansible to recognize the plugin
# InventoryPlugin()