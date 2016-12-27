<h1>Asa Lib 1.0</h1>
[![Build Status](https://travis-ci.org/Flexin1981/AsaLib.svg?branch=master)](https://travis-ci.org/Flexin1981/AsaLib)

Python Module to control the Asa via Ssh.

<h2>Requirements</h2>

paramiko 1.16.1<br>
netaddr 0.7.18

<h2>Usage</h2>

Below is an example usage of the module.

    from asa_lib import Asa
    
    asa = Asa('192.168.1.1', 'username', 'password', 'enable')
    asa.login()
    asa.set_enable_mode()
    asa.set_terminal_pager(0)
    asa.get_configuration()
    
    
<h3>HostName</h3>

Getting Hostname

    print asa.hostname
    
    or 
    
    print asa.get_hostname()
    
Setting Hostname

    asa.hostname = "This_hostname"
    
    or 
    
    asa.set_hostname("this_hostname")
    
<h3>Enable Password</h3>

Getting Enable password

    print asa.enable_password
    
    or 
    
    print asa.get_enable_password()
    
Setting Enable password

    asa.enable_password = "password"
    
    or 
    
    asa.set_enable_password("password")
    
<h3>Reloading the device</h3>

    asa.reload(<optional delay>)
    
Cancelling the reload

    asa.cancel_reload()
    

    

