import re


class StaticRoutes(object):

    generator = None

    def __init__(self):
        """
            List style object to hold all the static routes on the device.
        """
        self._routes = list()

    def __iter__(self):
        self.generator = None
        return self

    def next(self):
        if not self.generator:
            self.generator = self._gen()
        return self.generator.next()

    def _gen(self):
        for item in self._routes:
            yield item

    def _track_positions(self):
        for num, item in enumerate(self._routes):
            item._pos = num

    @staticmethod
    def _set_route_device(route):
        route.set_route()

    def append(self, route):
        """
            Add a route to the device.
        :param route: StaticRoute
        :return:
        """
        if type(route) != StaticRoute:
            raise TypeError
        self._set_route_device(route)
        self._routes.append(route)

    def remove(self, index):
        """
            Remove a route from the device by the index.
        :param index: int
        :return:
        """
        self._routes[index].unset_route()
        del self._routes[index]


class StaticRoute(object):

    STATIC_ROUTE_COMMANDS = {
        'route_command': 'route {0} {1} {2} {3}', 'get_routes': 'show run route'
    }

    def __init__(self, parent, interface=None, network=None, next_hop=None):
        """
            This is the object that represents the static route on the Asa device.

            You can add routes to the device in one of the following way;

            After Creating the Asa Device, logging in etc.

                route = StaticRoute(<route details>)
                asa.static_routes.append(route)

            One thing to note on this is that the routes are tracking the route that they maintain by a counter on this
            class, I should change this to ensure that the counter stays in sync with deletions, but have not done so
            yet, I would suggest that if a route is removed that the Asa get_routes is called to re sync the objects to
            the device, till a better solution is devised.

        :param interface: str
        :param network: IpNetwork
        :param next_hop: IpAddress
        """
        self._pos = None
        self._parent = parent

        self._raw_configuration = None
        self._interface = self._check_type_interface_name(interface)
        self._ip_network = network
        self._forwarding_address = next_hop

    @staticmethod
    def _check_type_interface_name(interface):
        from asa_modules.asa_interface import AsaInterface
        if type(interface) == str:
            return interface
        elif type(interface) == AsaInterface:
            return str(interface)
        elif interface is None:
            return None
        else:
            raise TypeError

    def _get_route(self):
        return re.findall(
            'route (.*)', self._parent.ssh_session.send_command(self.STATIC_ROUTE_COMMANDS['get_routes'])
        )[self.pos]

    def _parse_route(self):
        pass

    def set_route(self):
        """
            Method to set the route on the device , this should only be called once.
        :return:
        """
        self._parent.set_config_mode()
        self._parent.ssh_session.send_command(
            self.STATIC_ROUTE_COMMANDS['route_command'].format(
                self._interface, str(self._ip_network.ip), str(self._ip_network.netmask),
                str(self._forwarding_address)
            )
        )
        self._parent.unset_config_mode()

    def unset_route(self):
        """
            Method to uset the route on the device, this object should be removed from the StaticRoutes object once
            so that the Asa class stays in sync with the device.
        :return:
        """
        self._parent.set_config_mode()
        self._parent.ssh_session.send_command(
            'no ' + self.STATIC_ROUTE_COMMANDS['route_command'].format(
                self._interface, str(self._ip_network.ip), str(self._ip_network.netmask),
                str(self._forwarding_address)
            )
        )
        self._parent.unset_config_mode()
