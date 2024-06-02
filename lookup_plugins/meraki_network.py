# python 3 headers, required if submitting to Ansible
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r"""
  name: file
  author: Steven Carter (@stevenca) <stevenca@cisco.com>
  version_added: "0.9"  # for collections, use the collection version, not the Ansible version
  short_description: Find Meraki Network by ID
  description:
      - This lookup returns the network given then newtork ID.
  options:
    _terms:
      description: path(s) of files to read
      required: True
    lookup_key:
      description:
            - The key to use for the lookup.
            - This one can be set directly ``key='x'`` or in ansible.cfg, but can also use vars or environment.
      type: string
      default: name
      ini:
        - section: meraki_network
          key: lookup_key
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

        # consume an option: if this did something useful, you can retrieve the option value here
        if self.get_option('lookup_key'):
            lookup_key = self.get_option('lookup_key')
        else:
            lookup_key = "name"

        meraki_api_key = os.environ.get('MERAKI_DASHBOARD_API_KEY')
        meraki_base_url = os.environ.get('MERAKI_BASE_URL')
        meraki_org_id = os.environ.get('MERAKI_ORG_ID')
        dashboard = meraki.DashboardAPI(api_key=meraki_api_key,
                                            base_url=meraki_base_url,
                                            output_log=False,
                                            log_file_prefix=os.path.basename(__file__)[:-3],
                                            log_path='',
                                            print_console=False)

        meraki_networks = dashboard.organizations.getOrganizationNetworks(
            meraki_org_id, total_pages='all'
        )

        # lookups in general are expected to both take a list as input and output a list
        # this is done so they work with the looping construct 'with_'.
        ret = []
        for term in terms:
            display.debug("Looking up network: %s" % term)

            # Find the network with the requested network ID
            for network in meraki_networks:
                if network[lookup_key] == term:
                    ret.append(network)
                    continue
        return ret