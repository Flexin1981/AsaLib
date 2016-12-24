from asa_modules.asa_base import AsaBase
from asa_modules.asa_interface import AsaInterfaces, AsaInterface
from asa_modules.routing.static_route import StaticRoutes, StaticRoute
from asa_modules.asa_users import AsaUsers, AsaUser
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

    @property
    def users(self):
        if not self._users:
            self._users = AsaUsers()
            self.get_users()
        return self._users

    def __init__(self, hostname, username, password, enable):
        super(Asa, self).__init__(hostname, username, password, enable)
        self._interfaces = None
        self._static_routes = None
        self._users = None

        self._raw_configuration = None

    def get_configuration(self):
        self._raw_configuration = self.ssh_session.send_command(self.ASA_COMMANDS['get_running_configuration'])

    def get_hostname(self):
        self._hostname = re.search(
            'hostname[\s](.*)', self.ssh_session.send_command(self.COMMAND_LIST['get_hostname'])
        ).group(1)

    def set_hostname(self, hostname):
        self.set_config_mode()
        self.ssh_session.send_command(hostname)
        self.unset_config_mode()

    def get_interfaces(self):
        return {
            interface: AsaInterface(interface) for interface in re.findall('interface (.*)', self._raw_configuration)
        }

    def get_static_routes(self):
        for _ in re.findall('route .* 1', self._raw_configuration):
            self.static_routes.append(StaticRoute(self))

    def get_users(self):
        for _ in re.findall('username .*', self._raw_configuration):
            self.users.append(AsaUser(self))


if __name__ == '__main__':
    asa = Asa('10.0.0.1', 'john', 'john', '')
    asa.login()
    asa.set_enable_mode()
    asa.set_terminal_pager(0)
    asa.get_configuration()

    asa.get_hostname()
    print asa.hostname

