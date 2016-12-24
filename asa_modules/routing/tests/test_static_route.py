import unittest
import asa_modules.ssh
from asa_tests.mock_ssh import MockSsh
asa_modules.ssh.Ssh = MockSsh
from asa_lib import Asa
from netaddr import IPNetwork, IPAddress
Asa.Ssh = MockSsh
from asa_modules.routing.static_route import StaticRoute


class TestAsaStaticRoutes(unittest.TestCase):

    def setUp(self):
        self.asa = Asa('192.168.0.1', 'john', 'uber_secure_pw', '')
        self.asa.login()
        self.asa.set_enable_mode()
        self.asa.set_terminal_pager(0)
        self.asa.get_configuration()

    def test_static_route_fails_if_not_static_route_type(self):
        with self.assertRaises(TypeError):
            self.asa.static_routes.append('')

    def test_static_route_gets_added_to_list_str_type(self):
        length_before_test = len(self.asa.static_routes._routes)
        self.asa.static_routes.append(
            StaticRoute(self.asa, 'outside', IPNetwork('192.168.1.0/24'), IPAddress('192.168.0.254'))
        )
        self.assertEquals(
            length_before_test + 1, len(self.asa.static_routes._routes)
        )
