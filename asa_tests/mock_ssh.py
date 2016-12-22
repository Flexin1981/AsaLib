

class MockSsh(object):

    def __init__(self, hostname, username, password):
        self.hostname = hostname
        self.username = username
        self.password = password

    def send_command(self, command, results=True):
        if command == 'show run hostname':
            return 'test_hostname'
