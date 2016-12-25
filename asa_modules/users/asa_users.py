import re


class AsaUsers(object):

    def __init__(self):
        self._users = []

    def _track_positions(self):
        for num, item in enumerate(self._users):
            item._pos = num

    def append(self, value):
        if type(value) != AsaUser:
            raise TypeError('User should be AsaUser Type')
        value.set_user()
        self._users.append(value)
        self._track_positions()

    def remove(self, index):
        self._users[index].unset_user()
        del self._users[index]
        self._track_positions()


class AsaUser(object):

    ASA_USERNAME_COMMANDS = {
        'username': 'username {0} password {1} privilage {2}'
    }

    def __init__(self, parent, username=None, password=None, privilege=None):
        self._parent = parent
        self._pos = None

        self._username = username
        self._password = password
        self._privilege = privilege

    def _find_user(self):
        return re.findall(
            'username[\s](.*?)[\s]password[\s](.*)(?:[\s]privilage[\s]|)(.*)', self._parent._raw_configuration
        )[self._pos]

    def _get_user(self):
        user = self._find_user()
        self._username = user[0]
        self._password = user[1]
        self._privilage = user[2]

    def set_user(self):
        self._parent.set_config_mode()
        self._parent.ssh_session.send_command(
            self.ASA_USERNAME_COMMANDS['username'].format(self._username, self._password, str(self._privilege))
        )
        self._parent.unset_config_mode()

    def unset_user(self):
        self._parent.set_config_mode()
        self._parent.ssh_session.send_command(
            'no ' + self.ASA_USERNAME_COMMANDS['username'].format(self._username, self._password, str(self._privilege))
        )
        self._parent.unset_config_mode()
