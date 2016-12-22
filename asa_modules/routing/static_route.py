import re


class StaticRoutes(object):

    def __init__(self):
        self._routes = list()

    def __iter__(self):
        return self

    def next(self):
        pass

    def append(self, value):
        value.set_route()
        self._routes.append(value)

    def remove(self, index):
        self._routes[index].unset_route()
        self._routes.remove(index)


class StaticRoute(object):

    # There is going to be an issue with this class if routes get deleted, as the indexing with not follow once this is
    # done, the only option that I can see if a route gets deleted is to throw all existing objects and rebuild them.

    INDEXES = 0

    STATIC_ROUTE_COMMANDS = {
        'route_command': 'route {0} {1} {2} {3}', 'get_routes': 'show run route'
    }

    def __init__(self):
        self._id = self._set_class_count_varibale()

        self._raw_configuration = None
        self._interface = None
        self._ip_network = None
        self._forwarding_address = None

    @staticmethod
    def _set_class_count_varibale():
        StaticRoute.INDEXES += 1
        return StaticRoute.INDEXES

    def _get_route(self):
        return re.findall(
            'route (.*)', self.ssh_session.send_command(self.STATIC_ROUTE_COMMANDS['get_routes'])
        )[self._id]

    def _parse_route(self):
        pass

    def set_route(self):
        self._set_config_mode()
        self.ssh_session.send_command(
            self.STATIC_ROUTE_COMMANDS['route_command'].format(
                self._interface, str(self._ip_network.ip), str(self._ip_network.netmask),
                str(self._forwarding_address.ip)
            )
        )
        self._unset_config_mode()

    def unset_route(self):
        self._set_config_mode()
        self.ssh_session.send_command(
            'no ' + self.STATIC_ROUTE_COMMANDS['route_command'].format(
                self._interface, str(self._ip_network.ip), str(self._ip_network.netmask),
                str(self._forwarding_address.ip)
            )
        )
        self._unset_config_mode()
