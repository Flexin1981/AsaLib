import re


class StaticRoutes(object):

    def __init__(self):
        """
            List style object to hold all the static routes on the device.
        """
        self._routes = list()

    def __iter__(self):
        return self

    def next(self):
        pass

    def append(self, route):
        """
            Add a route to the device.
        :param route: StaticRoute
        :return:
        """
        route.set_route()
        self._routes.append(route)

    def remove(self, index):
        """
            Remove a route from the device by the index.
        :param index: int
        :return:
        """
        self._routes[index].unset_route()
        self._routes.remove(index)


class StaticRoute(object):

    INDEXES = 0

    STATIC_ROUTE_COMMANDS = {
        'route_command': 'route {0} {1} {2} {3}', 'get_routes': 'show run route'
    }

    def __init__(self, interface=None, network=None, next_hop=None):
        """
            This is the object that represents the static route on the Asa device.

            One thing to note on this is that the routes are tracking the route that they maintain by a counter on this
            class, I should change this to ensure that the counter stays in sync with deletions, but have not done so
            yet, I would suggest that if a route is removed that the Asa get_routes is called to re sync the objects to
            the device, till a better solution is devised.

        :param interface: str
        :param network: IpNetwork
        :param next_hop: IpAddress
        """
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
        """
            Method to set the route on the device , this should only be called once.
        :return:
        """
        self._set_config_mode()
        self.ssh_session.send_command(
            self.STATIC_ROUTE_COMMANDS['route_command'].format(
                self._interface, str(self._ip_network.ip), str(self._ip_network.netmask),
                str(self._forwarding_address.ip)
            )
        )
        self._unset_config_mode()

    def unset_route(self):
        """
            Method to uset the route on the device, this object should be removed from the StaticRoutes object once
            so that the Asa class stays in sync with the device.
        :return:
        """
        self._set_config_mode()
        self.ssh_session.send_command(
            'no ' + self.STATIC_ROUTE_COMMANDS['route_command'].format(
                self._interface, str(self._ip_network.ip), str(self._ip_network.netmask),
                str(self._forwarding_address.ip)
            )
        )
        self._unset_config_mode()
