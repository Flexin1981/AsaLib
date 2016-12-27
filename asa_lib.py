import re

from asa_modules.asa_base import AsaBase
from asa_modules.asa_interface import AsaInterfaces, AsaInterface
from asa_modules.routing.static_route import StaticRoutes, StaticRoute
from asa_modules.users.asa_users import AsaUsers, AsaUser


class Asa(AsaBase):

    ASA_COMMANDS = {
        'get_running_configuration': 'show run', 'reload': 'reload in {0} noconfirm', 'cancel_reload': 'reload cancel',
        'enable password': 'enable password {0}'
    }

    @property
    def enable_password(self):
        if not self._enable_password:
            self._enable_password = self.get_enable_password()
        return self._enable_password

    @enable_password.setter
    def enable_password(self, password):
        self.set_enable_password(password)
        self.get_enable_password()

    @property
    def hostname(self):
        if not self._hostname:
            self.get_hostname()
        return self._hostname

    @hostname.setter
    def hostname(self, hostname):
        self.set_hostname(hostname)
        self.get_hostname()

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
        return self._users

    def __init__(self, hostname, username, password, enable):
        super(Asa, self).__init__(hostname, username, password, enable)
        self._interfaces = None
        self._static_routes = None
        self._users = AsaUsers(self)
        self._enable_password = None

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
        self.static_routes._routes = [StaticRoute(self) for _ in re.findall('route .* 1', self._raw_configuration)]

    def get_users(self):
        self.users.get()

    def reload(self, delay_time=0):
        """
            Reload the device with an optional delay in seconds
        :param delay_time:
        :return:
        """
        hours, minutes = divmod(delay_time, 60)
        self.ssh_session.send_command(self.ASA_COMMANDS['reload'].format(str(hours) + ':' + str(minutes)))
        return True

    def cancel_reload(self):
        """
            Cancel a Delayed reload.
        :return:
        """
        self.ssh_session.send_command(self.ASA_COMMANDS['cancel_reload'])
        return True

    def get_enable_password(self):
        return self.ssh_session.send_command('show run enable')

    def set_enable_password(self, password):
        self.set_config_mode()
        self.ssh_session.send_command(self.ASA_COMMANDS['enable password'].format(password))
        self.unset_config_mode()
        return True
