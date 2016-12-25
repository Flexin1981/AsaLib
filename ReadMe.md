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
    
<h3>Adding a local username</h3>

Once you have logged in just append a AsaUser object to the users field of the asa, and ensure that you pass the parent 
asa in.
    
    asa.users.append(
        AsaUser(asa, 'john', 'uber_pw', 15)
    )
        
<h3>Removing a local username</h3>

All you have to do is call the remove function on the users object in the asa and pass the index in.

    asa.users.remove(0)
