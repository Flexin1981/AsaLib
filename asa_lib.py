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
            self._get_hostname()
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

    def __init__(self, hostname, username, password):
        super(Asa, self).__init__(hostname, username, password)
        self._get_configuration()

        self._interfaces = None
        self._static_routes = None

    def _get_configuration(self):
        self._raw_configuration = self.ssh_session.send_command(self.ASA_COMMANDS['get_running_configuration'])

    def _get_hostname(self):
        self._hostname = self.ssh_session.send_command(self.COMMAND_LIST['get_hostname'])

    def set_hostname(self, hostname):
        self._set_config_mode()
        self.ssh_session.send_command(hostname)
        self._unset_config_mode()

    def get_interfaces(self):
        return {
            interface: AsaInterface(interface) for interface in re.findall('Interface (.*)', self._raw_configuration)
        }

    def get_static_routes(self):
        for _ in re.findall('route .* 1', self._raw_configuration):
            self.static_routes.append(StaticRoute(self))
