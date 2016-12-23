from asa_modules.asa_base import AsaBase
from asa_modules.asa_interface import AsaInterfaces, AsaInterface
from asa_modules.routing.static_route import StaticRoutes, StaticRoute
import re


class Asa(AsaBase):

    ASA_COMMANDS = {
        'get_running_configuration': 'show run'
    }

    @property
    def hostname(self):
        if not self._hostname:
            self.get_hostname()
        return self._hostname

    @property
    def interfaces(self):
        if not self._interfaces:
            self._interfaces = AsaInterfaces(self.get_interfaces())
        return self._interfaces

    @property
    def static_routes(self):
        if not self._static_routes:
            self._static_routes = StaticRoutes()
            self.get_static_routes()
        return self._static_routes

    def __init__(self, hostname, username, password, enable):
        super(Asa, self).__init__(hostname, username, password, enable)
        self._interfaces = None
        self._static_routes = None



    def get_configuration(self):
        self._raw_configuration = self.ssh_session.send_command(self.ASA_COMMANDS['get_running_configuration'])

    def get_hostname(self):
        self._hostname = self.ssh_session.send_command(self.COMMAND_LIST['get_hostname'])

    def set_hostname(self, hostname):
        self._set_config_mode()
        self.ssh_session.send_command(hostname)
        self.unset_config_mode()

    def get_interfaces(self):
        return {
            interface: AsaInterface(interface) for interface in re.findall('interface (.*)', self._raw_configuration)
        }

    def get_static_routes(self):
        for _ in re.findall('route .* 1', self._raw_configuration):
            self.static_routes.append(StaticRoute(self))


if __name__ == '__main__':
    asa = Asa('10.0.0.1', 'john', 'john', '')
    asa.login()
    asa.set_enable_mode()
    asa.set_terminal_pager(0)
    asa.get_configuration()

    print asa.interfaces._interfaces[0].ip_address
