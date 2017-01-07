import re
from netaddr import IPNetwork, IPAddress


class AsaInterfaces(object):

    ASA_INTERFACE_COMMANDS = {
        'show': 'show run int'
    }

    def _collect_interfaces(self):
        return self.parent.ssh_session_send_command(self.ASA_INTERFACE_COMMANDS['show'])

    @staticmethod
    def _check_interface_type(interface):
        if type(interface) != AsaInterface:
            raise TypeError('Interface should be of type AsaInterface')

    def _is_interface_removable(self, interface):
        if getattr(self, interface).removable:
            return True
        else:
            return False

    def get_interfaces(self):
        for interface in re.findall('(interface .*?)!', self._raw_configuration, re.DOTALL):
            setattr(
                self, re.search('interface (.*)', interface).group(1),
                AsaInterface(self.parent, re.search('interface (.*)', interface).group(1))
            )

    def append(self, interface):
        self._check_interface_type(interface)
        setattr(self, interface.interface, interface)

    def remove(self, interface_name):
        if self._is_interface_removable(interface_name):
            getattr(self, interface_name).delete_interface()
            delattr(self, interface_name)

    def __init__(self, parent):
        self.parent = parent
        self._raw_configuration = self._collect_interfaces()
        self.get_interfaces()


class AsaInterface(object):

    # Todo; need to add setter commands to the AsaInterface
    # Todo; Need to add parent to the AsaInterface object.
    # Todo: Need to ad a non removal property so that physical interfaces cannot be removed.

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

    @ip_address.setter
    def ip_address(self, value):
        self.set_ip_address(value)

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
        if not self._is_shut:
            self._status = self._get_interface_state()
        return self._status

    def __init__(
            self, parent, interface_id, name_if=None, ip_address=None, security_level=0, is_shut=True,  removable=True
    ):
        self.interface = interface_id
        self._removable = removable

        if self._check_parent_type(parent):
            self._parent = parent

        self._ip_address = ip_address
        self._security_level = security_level
        self._name_if = name_if
        self._is_shut = is_shut

    def __str__(self):
        return self.name_if

    @staticmethod
    def _check_parent_type(parent):
        from asa_lib import Asa
        if type(parent) != Asa:
            raise TypeError('Parent type should be an instace of Asa')
        return True

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
        self.parent.ssh_session.send_command(
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

    def delete_interface(self):
        # Todo; need to impliment this method.
        pass
