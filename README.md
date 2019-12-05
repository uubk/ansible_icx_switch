# icx_switch
Opinionated default config for Brocade/Broadcom/Ruckus ICX-series switches.
Use the new-ish `icx_*` ansible modules as far as currently possible. Tested
on ICX-7150, ICX-7250 and ICX-6430.

## Configuration
| Name | Default value | Description |
| ---- | ------------- | ----------- |
| `icx_my_name` | `testswitch` | Hostname to set on the switch |
| `icx_mgmt_ip` | `1.2.3.4/24` | IP to configure in VLAN 1 |
| `icx_default_gw` | `1.2.3.4` | Default gateway to use |
| `icx_nameserver` | `8.8.8.8` | Nameserver to use |
| `icx_domain_name` | `example.org` | Domain name to configure |
| `icx_is_l3_switch` | `True` | Whether this is one of the new (71xx) L3 switches |
| `icx_ntp_servers` | `[216.239.35.0, 216.239.35.4]` | List of NTP servers |
| `icx_snmp_enable` | `False` | Whether to enable a simple SNMP config |
| `icx_snmp_user` | `abc` | SNMP user to set up |
| `icx_snmp_password` | `def` | SNMP password to set up |
| `icx_snmp_host` | `1.2.3.4` | SNMP host to grant access |
| `icx_snmp_privs` | `read all write none notify none` | Access to grant |
| `icx_expected_firmware` | `08.0.92T213` | Firmeware version to require. If set to `""` the check is ignored |
| `icx_users` | (see `defaults/main.yml`) | Users to create (see below) |
| `icx_vlans` | (see `defaults/main.yml`) | VLANs to create (see below) |
| `icx_portconfig` | (see `defaults/main.yml`) | Port configuration (see below) |
| `icx_lags` | (see `defaults/main.yml`) | LAGs to create (see below) |

### Port config
Example:
```
foo:
- &default_access_port
    type: access
    tagged: []
    untagged:
      - 2
- &all_vlan_trunk
    tagged:
      - 2
      - 3
      - 4
      - 5
      - 6
      - 7
      - 8
      - 4080
    untagged:
      - 1
icx_portconfig:
  - name: accessFibre3
    port: 1/2/5
    link: fibre
    << : *default_access_port
  - name: max-sw
    port: 1/2/6
    link: fibre
    type: access
    << : *all_vlan_trunk
```
Each portconfig entry has the following attributes:
 * name: ASCII string to identify the port. This is copied to the switch
 * link: 'fibre' will skip EEE setup and possibly configure DDM in the future.
 * type: currently, 'trust' will trust for dhcp snooping etc.
 * port: port identiefier as per switch syntax. Ethernet will be automatically prepended
 * untagged: Untagged VLAN to use
 * tagged: Tagged VLAN to use

### LAG config
```
icx_lags:
  - name: test-lag
    id: 1
    ports: ethe 1/2/1 to 1/2/2
    type: access
    tagged: []
    untagged:
      - 2
```
LAG configs work similar to normal ports, except that you have to specify the
ports they cover in `ports` and _must not_ configure the ports themselves
via `icx_portconfig`!

### VLAN config
```
icx_vlans:
  - name: FancyNet
    id: 2
```
Only `id` and `name` are supported. The actual port membership is calculated
via custom filter, so you can pretend that VLAN membership works on port like
it does on most other switches ;) The python code for this is in
`filter_plugins`, just in case it's not loaded for some reason...

### Users
```
icx_users:
  - name: foo
    configured_password: bar
    update_password: on_create
    state: present
    privilege: "0"
```
Pretty self-explanatory. The arguments are simply passed through to the [ansible
module](https://docs.ansible.com/ansible/latest/modules/icx_user_module.html#icx-user-module).

## License
Apache 2.0
