import unittest
import asa_modules.ssh
from asa_tests.mock_ssh import MockSsh
asa_modules.ssh.Ssh = MockSsh
from asa_lib import Asa
Asa.Ssh = MockSsh

from asa_modules.users.asa_users import AsaUser


class TestAsaUsers(unittest.TestCase):

    def setUp(self):
        self.asa = Asa('192.168.0.1', 'john', 'uber_secure_pw', '')
        self.asa.login()
        self.asa.set_enable_mode()
        self.asa.set_terminal_pager(0)
        self.asa.get_configuration()

    def test_append_fails_if_user_obj_not_passed_in(self):
        with self.assertRaises(TypeError):
            self.asa.users.append('')

    def test_append_increases_length_of_object(self):
        self.asa.get_users()
        length_before_test = len(self.asa.users._users)
        self.asa.users.append(
            AsaUser(self.asa, 'john', 'uber_pw', 15)
        )
        self.assertEquals(
            length_before_test + 1, len(self.asa.users._users)
        )

    def test_length_of_array_decreases(self):
        self.asa.get_users()
        self.asa.users.append(
            AsaUser(self.asa, 'john', 'uber_pw', 15)
        )
        length_before_test = len(self.asa.users._users)
        self.asa.users.remove(0)
        self.assertEquals(
            length_before_test - 1, len(self.asa.users._users)
        )
