import re


class AsaUsers(object):

    UREGEX = 'username[\s](.*?)[\s]password[\s](.*?)[\s](?:privilage[\s]([\d]+)|)'
    USERNAMES_COMMANDS = {
        'running': 'show run usernames'
    }

    def __init__(self, parent):
        self.raw_configuration = None
        self._users = []
        self.parent = parent

    def append(self, value):
        if type(value) != AsaUser:
            raise TypeError('User should be AsaUser Type')
        value.set_user()
        self._users.append(value)
        self.get()

    def get(self):
        self._users = []
        for num, x in enumerate(
                re.findall(self.UREGEX, self.parent.ssh_session.send_command(self.USERNAMES_COMMANDS['running']))
        ):
            self._users.append(AsaUser(self.parent, x[0], x[1], x[2], num))

    def remove(self, index):
        self._users[index].unset_user()
        del self._users[index]
        self.get()


class AsaUser(object):

    ASA_USERNAME_COMMANDS = {
        'username': 'username {0} password {1} privilage {2}'
    }

    def __init__(self, parent, username=None, password=None, privilege=None, position=None):
        self.parent = parent
        self._check_parent_type()
        self._pos = None

        self._username = username
        self._password = password
        self._privilege = privilege

    def _check_parent_type(self):
        from asa_lib import Asa
        assert type(self.parent) == Asa

    def set_user(self):
        self.parent.set_config_mode()
        self.parent.ssh_session.send_command(
            self.ASA_USERNAME_COMMANDS['username'].format(self._username, self._password, str(self._privilege))
        )
        self.parent.unset_config_mode()

    def unset_user(self):
        self.parent.set_config_mode()
        self.parent.ssh_session.send_command(
            'no ' + self.ASA_USERNAME_COMMANDS['username'].format(self._username, self._password, str(self._privilege))
        )
        self.parent.unset_config_mode()
