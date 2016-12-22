import re
from asa_base import ConfigurationError


class TunnelGroup(object):

    TUNNEL_GROUP_COMMAND_LIST = {
        'get_tunnel_group_configuration': 'show run tunnel-group {0}'
    }

    @property
    def type(self):
        if not self._type:
            self._type = self._get_type()
        return self._type

    def __init__(self, tunnel_group_id=None):
        self._id = tunnel_group_id

        self._raw_configuration = None
        self._type = None

        if tunnel_group_id:
            self._get_configuration()

    def _get_configuration(self):
        self._raw_configuration = self.ssh_session.send_command(
            self.TUNNEL_GROUP_COMMAND_LIST['get_tunnel_group_configuration']
        )

    def _get_type(self):
        return re.search('type (.*)', self._raw_configuration).group(1)

    def set_type(self, type):
        if self.type:
            raise ConfigurationError("tunnel-group type cannot be changed once set")






class GeneralAttributes(object):
    pass


class IpSecAttributes(object):
    pass
