# meraki-automation

## Site Provisioning
```
ansible-playbook provision-site.yml -e site_name=cpn-gov-nashville
```

```
ansible-playbook claim-devices.yml -e serials=Q3FA-466B-PWVU,Q4CD-KYWB-AEDQ,Q5AA-VHDD-RMXZ --limit=cpn_gov_nashville
```

```
ansible-playbook provision-appliance.yml --limit=cpn_gov_nashville
```

```
ansible-playbook check-network-status.yml --limit=cpn_gov_nashville -e wait=true
```

```
ansible-playbook update-switch-ports.yml --limit=cpn_gov_nashville
```