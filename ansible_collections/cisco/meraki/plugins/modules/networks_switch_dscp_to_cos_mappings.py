#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2021, Cisco Systems
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: networks_switch_dscp_to_cos_mappings
short_description: Resource module for networks _switch _dscptocosmappings
description:
- Manage operation update of the resource networks _switch _dscptocosmappings.
- Update the DSCP to CoS mappings.
version_added: '2.16.0'
extends_documentation_fragment:
  - cisco.meraki.module
author: Francisco Munoz (@fmunoz)
options:
  mappings:
    description: An array of DSCP to CoS mappings. An empty array will reset the mappings
      to default.
    elements: dict
    suboptions:
      cos:
        description: The actual layer-2 CoS queue the DSCP value is mapped to. These
          are not bits set on outgoing frames. Value can be in the range of 0 to 5 inclusive.
        type: int
      dscp:
        description: The Differentiated Services Code Point (DSCP) tag in the IP header
          that will be mapped to a particular Class-of-Service (CoS) queue. Value can
          be in the range of 0 to 63 inclusive.
        type: int
      title:
        description: Label for the mapping (optional).
        type: str
    type: list
  networkId:
    description: NetworkId path parameter. Network ID.
    type: str
requirements:
- meraki >= 2.4.9
- python >= 3.5
seealso:
- name: Cisco Meraki documentation for switch updateNetworkSwitchDscpToCosMappings
  description: Complete reference of the updateNetworkSwitchDscpToCosMappings API.
  link: https://developer.cisco.com/meraki/api-v1/#!update-network-switch-dscp-to-cos-mappings
notes:
  - SDK Method used are
    switch.Switch.update_network_switch_dscp_to_cos_mappings,

  - Paths used are
    put /networks/{networkId}/switch/dscpToCosMappings,
"""

EXAMPLES = r"""
- name: Update all
  cisco.meraki.networks_switch_dscp_to_cos_mappings:
    meraki_api_key: "{{meraki_api_key}}"
    meraki_base_url: "{{meraki_base_url}}"
    meraki_single_request_timeout: "{{meraki_single_request_timeout}}"
    meraki_certificate_path: "{{meraki_certificate_path}}"
    meraki_requests_proxy: "{{meraki_requests_proxy}}"
    meraki_wait_on_rate_limit: "{{meraki_wait_on_rate_limit}}"
    meraki_nginx_429_retry_wait_time: "{{meraki_nginx_429_retry_wait_time}}"
    meraki_action_batch_retry_wait_time: "{{meraki_action_batch_retry_wait_time}}"
    meraki_retry_4xx_error: "{{meraki_retry_4xx_error}}"
    meraki_retry_4xx_error_wait_time: "{{meraki_retry_4xx_error_wait_time}}"
    meraki_maximum_retries: "{{meraki_maximum_retries}}"
    meraki_output_log: "{{meraki_output_log}}"
    meraki_log_file_prefix: "{{meraki_log_file_prefix}}"
    meraki_log_path: "{{meraki_log_path}}"
    meraki_print_console: "{{meraki_print_console}}"
    meraki_suppress_logging: "{{meraki_suppress_logging}}"
    meraki_simulate: "{{meraki_simulate}}"
    meraki_be_geo_id: "{{meraki_be_geo_id}}"
    meraki_use_iterator_for_get_pages: "{{meraki_use_iterator_for_get_pages}}"
    meraki_inherit_logging_config: "{{meraki_inherit_logging_config}}"
    state: present
    mappings:
    - cos: 1
      dscp: 1
      title: Video
    networkId: string

"""
RETURN = r"""
meraki_response:
  description: A dictionary or list with the response returned by the Cisco Meraki Python SDK
  returned: always
  type: dict
  sample: >
    {}
"""
