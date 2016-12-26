<h1>Asa Lib 1.0</h1>
[![Build Status](https://travis-ci.org/Flexin1981/AsaLib.svg?branch=master)](https://travis-ci.org/Flexin1981/AsaLib)

Python Module to control the Asa via Ssh.

<h2>Usage</h2>

Below is an example usage of the module.

    from asa_lib import Asa
    
    asa = Asa('192.168.1.1', 'username', 'password', 'enable')
    asa.login()
    asa.set_enable_mode()
    asa.set_terminal_pager(0)
    asa.get_configuration()

