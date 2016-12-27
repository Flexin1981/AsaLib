import unittest
import asa_modules.ssh
from asa_tests.mock_ssh import MockSsh
asa_modules.ssh.Ssh = MockSsh
from asa_lib import Asa

Asa.Ssh = MockSsh


class TestAsa(unittest.TestCase):

    def setUp(self):

        self.asa = Asa('192.168.0.1', 'john', 'uber_secure_pw', '')
        self.asa.login()
        self.asa.set_enable_mode()
        self.asa.set_terminal_pager(0)
        self.asa.get_configuration()

    def test_reload_returns_True(self):
        self.assertEquals(
            True, self.asa.reload()
        )

    def test_cancel_reload_returns_True(self):
        self.assertEquals(
            True, self.asa.cancel_reload()
        )

    def test_get_enable_password(self):
        self.assertEquals(
            'enable password GDHAGRHERH', self.asa.get_enable_password()
        )

    def test_set_enable_password(self):
        self.assertEquals(
            True, self.asa.set_enable_password('blah')
        )