from asa_modules.ssh import Ssh


class ConfigurationError(Exception):
    pass


class AsaBase(object):

    COMMAND_LIST = {
        'config_mode': 'config terminal', 'end_config_mode': 'end',
        'get_hostname': 'show run hostname', 'save_config': 'write memory', 'pager_command': 'terminal pager {0}',
        'enable': 'enable', 'diable': 'disable'
    }

    def __init__(self, hostname, username, password, enable):
        self.enable = enable
        self.ssh_session = Ssh(hostname, username, password)

        self._enable_set = False
        self._hostname = None

    def login(self):
        self.ssh_session.login()

    def set_enable_mode(self):
        if self.ssh_session.is_logged_in():
            self.ssh_session.send_command(self.COMMAND_LIST['enable'])
            self.ssh_session.send_command(self.enable)
            self._enable_set = True

    def unset_enable_mode(self):
        if self.ssh_session.is_logged_in():
            self.ssh_session.send_command(self.COMMAND_LIST['disable'])
            self._enable_set = False

    def is_enable_mode(self):
        return self._enable_set

    def set_terminal_pager(self, level=0):
        if self.ssh_session.is_logged_in():
            self.ssh_session.send_command(self.COMMAND_LIST['pager_command'].format(str(level)))

    def set_config_mode(self):
        self.ssh_session.send_command(self.COMMAND_LIST['config_mode'])

    def unset_config_mode(self):
        self.ssh_session.send_command(self.COMMAND_LIST['end_config_mode'])

    def save_running_configuration(self):
        self.ssh_session.send_command(self.COMMAND_LIST['save_config'])
