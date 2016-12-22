from asa_modules.ssh import Ssh


class ConfigurationError(Exception):
    pass


class AsaBase(object):

    COMMAND_LIST = {
        'config_mode': 'config terminal', 'end_config_mode': 'end',
        'get_hostname': 'show run hostname', 'save_config': 'write memory'
    }

    def __init__(self, hostname, username, password):
        self.ssh_session = Ssh(hostname, username, password)

        self._hostname = None

    def _set_config_mode(self):
        self.ssh_session.send_command(self.COMMAND_LIST['config_mode'])

    def _unset_config_mode(self):
        self.ssh_session.send_command(self.COMMAND_LIST['end_config_mode'])

    def save_running_configuration(self):
        self.ssh_session.send_command(self.COMMAND_LIST['save_config'])
