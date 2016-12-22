import unittest
from asa_lib import Asa
from asa_tests.mock_ssh import MockSsh


class TestAsaBase(unittest.TestCase):

    def setUp(self):
        self.asa = Asa('192.168.0.1', 'john', 'uber_secure_pw')
        self.asa.ssh_session = MockSsh('192.168.0.1', 'john', 'uber_secure_pw')

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

    def test_host_name_returns_string(self):
        self.assertEquals(
            'test_hostname', self.asa.hostname
        )