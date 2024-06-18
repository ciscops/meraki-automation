#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2021, Cisco Systems
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: ipsec_delete
short_description: Resource module for Ipsec Delete
description:
- Manage operation delete of the resource Ipsec Delete.
- Removes an enabled IPsec node connection.
version_added: '1.0.0'
extends_documentation_fragment:
  - cisco.ise.module
author: Rafael Campos (@racampos)
options:
  hostName:
    description: HostName path parameter. Hostname of the deployed node.
    type: str
  nadIp:
    description: NadIp path parameter. IP address of the NAD.
    type: str
requirements:
- ciscoisesdk >= 2.2.1
- python >= 3.5
notes:
  - SDK Method used are
    native_ipsec.NativeIpsec.remove_ipsec_connection,

  - Paths used are
    delete /api/v1/ipsec/{hostName}/{nadIp},

"""

EXAMPLES = r"""
- name: Delete by id
  cisco.ise.ipsec_delete:
    ise_hostname: "{{ise_hostname}}"
    ise_username: "{{ise_username}}"
    ise_password: "{{ise_password}}"
    ise_verify: "{{ise_verify}}"
    state: absent
    hostName: string
    nadIp: string

"""

RETURN = r"""
ise_response:
  description: A dictionary or list with the response returned by the Cisco ISE Python SDK
  returned: always
  type: dict
  sample: >
    {
      "authType": "string",
      "certId": "string",
      "configureVti": true,
      "createTime": "string",
      "espAhProtocol": "string",
      "hostName": "string",
      "id": "string",
      "iface": "string",
      "ikeReAuthTime": 0,
      "ikeVersion": "string",
      "link": {
        "href": "string",
        "rel": "string",
        "type": "string"
      },
      "localInternalIp": "string",
      "modeOption": "string",
      "nadIp": "string",
      "phaseOneDHGroup": "string",
      "phaseOneEncryptionAlgo": "string",
      "phaseOneHashAlgo": "string",
      "phaseOneLifeTime": 0,
      "phaseTwoDHGroup": "string",
      "phaseTwoEncryptionAlgo": "string",
      "phaseTwoHashAlgo": "string",
      "phaseTwoLifeTime": 0,
      "psk": "string",
      "remotePeerInternalIp": "string",
      "status": "string",
      "updateTime": "string"
    }
"""
