import unittest
import asa_modules.ssh
from asa_tests.mock_ssh import MockSsh
asa_modules.ssh.Ssh = MockSsh
from asa_lib import Asa

Asa.Ssh = MockSsh


class TestAsaBase(unittest.TestCase):

    def setUp(self):

        self.asa = Asa('192.168.0.1', 'john', 'uber_secure_pw', '')
        self.asa.login()
        self.asa.set_enable_mode()
        self.asa.set_terminal_pager(0)
        self.asa.get_configuration()

    def test_hostname(self):
        self.assertEquals(
            '192.168.0.1', self.asa.ssh_session.hostname
        )

    def test_username(self):
        self.assertEquals(
            'john', self.asa.ssh_session.username
        )

    def test_password(self):
        self.assertEquals(
            'uber_secure_pw', self.asa.ssh_session.password
        )
