# Default Imports
import paramiko
from paramiko.py3compat import u
import logging
import socket

logger = logging.getLogger(__name__)


class NotLoggedInError(Exception):
    pass


class Ssh(object):

    def __init__(self, hostname, username, password):

        self.hostname = hostname
        self.username = username
        self.password = password

        self.ssh_client = paramiko.SSHClient()
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self._ssh_channel = None

    def __del__(self):
        self.logout()

    def login(self):
        self.ssh_client.connect(
            hostname=self.hostname, port=22, username=self.username, password=self.password,
            look_for_keys=False, allow_agent=False
        )
        self._ssh_channel = self.ssh_client.invoke_shell(width=400, height=40000)

    def is_logged_in(self):
        try:
            return self.ssh_client.get_transport().is_active()
        except Exception as err:
            logger.exception("General Error: {0}".format(err))
            return False

    def logout(self):
        if self.is_logged_in():
            self.send_command('exit')

    def _write_to_channel(self, write_string):
        self._ssh_channel.makefile('wb').write(write_string + '\n')

    def _read_from_channel(self, maxbytes=1024):
        self._ssh_channel.settimeout(0.5)
        return_buffer = ''

        channel_data = u(self._ssh_channel.recv(maxbytes))

        while True:
            try:
                return_buffer += channel_data
                channel_data = u(self._ssh_channel.recv(maxbytes))
            except socket.timeout:
                return_buffer += channel_data
                break

        return return_buffer

    @staticmethod
    def _clean_command(command, result_string):
        return result_string.replace(command, '')

    def send_command(self, command, results=True):
        if not self.is_logged_in():
            raise NotLoggedInError()

        self._write_to_channel(command)

        if results:
            return self._clean_command(command, self._read_from_channel())

    def send_commands(self, commands, results=True):
        command_results_list = []

        for command in commands:
            command_results_list.append(self.send_command(command, results))

        if results:
            return command_results_list
