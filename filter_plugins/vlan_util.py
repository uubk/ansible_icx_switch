def vlan_membership(interfaces, lags):
    ''' Converts the interface and lag dicts to a vlan membership dict
    '''
    vlans = {}
    def ensureVlan(vlan):
        if vlan not in vlans:
            vlans[vlan] = {
                "tagged": [],
                "untagged": [],
            }
    def addAllMembers(portList, portPrefix, portName):
        for item in portList:
            if 'tagged' in item:
                for vlan in item['tagged']:
                    ensureVlan(vlan)
                    vlans[vlan]['tagged'].append(portPrefix + str(item[portName]))
            if 'untagged' in item:
                for vlan in item['untagged']:
                    ensureVlan(vlan)
                    vlans[vlan]['untagged'].append(portPrefix + str(item[portName]))
    addAllMembers(interfaces, 'ethernet ', 'port')
    addAllMembers(lags, 'lag ', 'id')
    return vlans

class FilterModule(object):
    def filters(self):
        return {'vlan_membership': vlan_membership}
