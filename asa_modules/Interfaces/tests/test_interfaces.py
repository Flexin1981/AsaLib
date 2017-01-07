import unittest
import asa_modules.ssh
from asa_tests.mock_ssh import MockSsh
asa_modules.ssh.Ssh = MockSsh
from asa_lib import Asa
from netaddr import IPNetwork, IPAddress
Asa.Ssh = MockSsh
from asa_modules.Interfaces.asa_interface import AsaInterface, AsaInterfaces


class TestAsaInterfaces(unittest.TestCase):

    def setUp(self):
        self.asa = Asa('192.168.0.1', 'john', 'uber_secure_pw', '')
        self.asa.login()
        self.asa.set_enable_mode()
        self.asa.set_terminal_pager(0)
        self.asa.get_configuration()
