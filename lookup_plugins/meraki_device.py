# python 3 headers, required if submitting to Ansible
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r"""
  name: file
  author: Steven Carter (@stevenca) <stevenca@cisco.com>
  version_added: "0.9"  # for collections, use the collection version, not the Ansible version
  short_description: Find Meraki device by ID
  description:
      - This lookup returns the device given the serial number.
  options:
    _terms:
      description: path(s) of files to read
      required: True
  notes:
    - if read in variable context, the file can be interpreted as YAML if the content is valid to the parser.
    - this lookup does not understand globbing --- use the fileglob lookup instead.
"""
from ansible.errors import AnsibleError, AnsibleParserError
from ansible.plugins.lookup import LookupBase
from ansible.utils.display import Display
import os
import meraki

display = Display()

class LookupModule(LookupBase):

    def run(self, terms, variables=None, **kwargs):

        # First of all populate options,
        # this will already take into account env vars and ini config
        self.set_options(var_options=variables, direct=kwargs)

        meraki_api_key = os.environ.get('MERAKI_DASHBOARD_API_KEY')
        meraki_base_url = os.environ.get('MERAKI_BASE_URL')
        meraki_org_id = os.environ.get('MERAKI_ORG_ID')
        dashboard = meraki.DashboardAPI(api_key=meraki_api_key,
                                            base_url=meraki_base_url,
                                            output_log=False,
                                            log_file_prefix=os.path.basename(__file__)[:-3],
                                            log_path='',
                                            print_console=False)

        # lookups in general are expected to both take a list as input and output a list
        # this is done so they work with the looping construct 'with_'.
        ret = []
        for term in terms:
            display.debug("Looking up serial: %s" % term)
            try:
                device = dashboard.devices.getDevice(term)
                ret.append(device)
            except meraki.exceptions.APIError as e:
                if e.status != 404:
                    display.debug(f"{e.status}, {e.reason}: {e.message}")
            
        return ret