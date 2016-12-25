import re
from netaddr import IPNetwork, IPAddress


class AsaInterfaces:

    def __init__(self, interfaces):
        self._interfaces = interfaces

    def __iter__(self):
        return self

    def next(self):
        for key, value in self._interfaces:
            yield value


class AsaInterface:

    INTERFACE_COMMANDS = {
        'interface_configuration_mode': 'interface {0}', 'show_interface_configuration': 'show run interface {0}',
        'set_ip_address': 'ip-address {0} {1}', 'set_security_level': 'security-level {0}',
        'set_name_if': 'name-if {0}', 'set_interface_state': '{0}shutdown',
        'set_standby_address': 'ip-address {0} {1} {2}'
    }

    @property
    def ip_address(self):
        if not self._ip_address:
            self._ip_address = self._get_ip_address()
        return self._ip_address

    @property
    def security_level(self):
        if not self._security_level:
            self._security_level = self._get_security_level()
        return self._security_level

    @property
    def name_if(self):
        if not self._name_if:
            self._name_if = self._get_name_if()
        return self._name_if

    @property
    def state(self):
        if not self._state:
            self._status = self._get_interface_state()
        return self._status

    def __init__(self, interface_id):
        self._id = interface_id
        self._get_raw_configuration()

        self._ip_address = None
        self._security_level = None
        self._name_if = None
        self._status = None

    def __str__(self):
        return self.name_if

    def _set_interface_configuration_mode(self):
        self._set_config_mode()
        self.ssh_session.send_command(self.INTERFACE_COMMANDS['interface_configuration_mode'].format(self._id))

    def _unset_interface_configuration_mode(self):
        self. _unset_config_mode()

    def _get_raw_configuration(self):
        self._raw_configuration = self.ssh_session.send_command(self.INTERFACE_COMMANDS['show_interface_configuration'])

    def _get_ip_address(self):
        return IPNetwork(
            re.search('ip addess (.*)', self._raw_configuration).group(1).replace('', '/')
        )

    def set_ip_address(self, ip_address):

        assert type(ip_address) == IPNetwork

        self._set_interface_configuration_mode()
        self.ssh_session.send_command(
            self.INTERFACE_COMMANDS['set_ip_address'].format(str(ip_address.ip), str(ip_address.netmask))
        )
        self._unset_interface_configuration_mode()

    def _get_security_level(self):
        return re.search('security-level (.*)', self._raw_configuration).group(1)

    def set_security_level(self, security_level):
        assert (type(security_level) == int) and (0 <= security_level <= 100)

        self._set_interface_configuration_mode()
        self.ssh_session.send_command(self.INTERFACE_COMMANDS['set_security_level'].format(str(security_level)))
        self._unset_interface_configuration_mode()

    def _get_name_if(self):
        return re.search('name-if (.*)', self._raw_configuration).group(1)

    def set_name_if(self, name_if):
        self._set_interface_configuration_mode()
        self.ssh_session.send_command(
            self.INTERFACE_COMMANDS['set_name_if'].format(name_if)
        )
        self._unset_interface_configuration_mode()

    def _get_interface_state(self):
        if 'shutdown' in self._raw_configuration:
            return 'shut'
        else:
            return 'unshut'

    def set_interface_state(self, state):
        states = {True: '', False: 'no '}
        self._set_interface_configuration_mode()
        self.ssh_session.send_command(self.INTERFACE_COMMANDS['set_interface_state'].format(states[state]))
        self._unset_interface_configuration_mode()

    def _get_standby_address(self):
        return IPAddress(re.search('standby (.*)', self._raw_configuration).group(1))

    def set_standby_address(self, ip_address, standby_address):
        self._set_interface_configuration_mode()
        self.ssh_session.send_command(
            self.INTERFACE_COMMANDS['set_standby_address'].format(
                str(ip_address.ip), str(ip_address.netmask), str(standby_address.ip)
            )
        )
        self._unset_interface_configuration_mode()
