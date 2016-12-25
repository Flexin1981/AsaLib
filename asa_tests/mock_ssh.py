sample_config = """
ASA Version 7.2(3)
!
hostname ciscoasa
domain-name default.domain.invalid
enable password shlxHOGhGlncPVRr encrypted
names
!
interface Vlan1
 nameif inside
 security-level 100
 ip address 172.10.20.1 255.255.255.0
!
interface Vlan2
 nameif outside
 security-level 0
 ip address 209.123.123.123 255.255.255.0
!
interface Ethernet0/0
 switchport access vlan 2
!
interface Ethernet0/1
!
interface Ethernet0/2
!
interface Ethernet0/3
!
interface Ethernet0/4
!
interface Ethernet0/5
!
interface Ethernet0/6
!
interface Ethernet0/7
!
passwd shlxHOGhGlncPVRr encrypted
ftp mode passive
dns domain-lookup outside
dns server-group DefaultDNS
 domain-name default.domain.invalid
access-list inside_nat0_outbound extended permit ip 172.10.20.1 255.255.255.0 192.168.1.0 255.255.255.0
access-list outside_2_cryptomap extended permit ip 172.10.20.1 255.255.255.0 192.168.1.0 255.255.255.0
pager lines 24
logging enable
logging asdm informational
mtu inside 1500
mtu outside 1500
icmp unreachable rate-limit 1 burst-size 1
asdm image disk0:/asdm-523.bin
no asdm history enable
arp timeout 14400
global (outside) 1 interface
nat (inside) 0 access-list inside_nat0_outbound
nat (inside) 1 0.0.0.0 0.0.0.0
route outside 0.0.0.0 0.0.0.0 209.123.123.123 1
timeout xlate 3:00:00
timeout conn 1:00:00 half-closed 0:10:00 udp 0:02:00 icmp 0:00:02
timeout sunrpc 0:10:00 h323 0:05:00 h225 1:00:00 mgcp 0:05:00 mgcp-pat 0:05:00
timeout sip 0:30:00 sip_media 0:02:00 sip-invite 0:03:00 sip-disconnect 0:02:00
timeout uauth 0:05:00 absolute
http server enable
http 172.10.20.1 255.255.255.0 inside
no snmp-server location
no snmp-server contact
snmp-server enable traps snmp authentication linkup linkdown coldstart
crypto ipsec transform-set ESP-3DES-MD5 esp-3des esp-md5-hmac
crypto map outside_map 2 match address outside_2_cryptomap
crypto map outside_map 2 set pfs
crypto map outside_map 2 set peer 166.122.222.111
crypto map outside_map 2 set transform-set ESP-3DES-MD5
crypto map outside_map 2 set nat-t-disable
crypto map outside_map interface outside
crypto isakmp identity address
crypto isakmp enable outside
crypto isakmp policy 10
 authentication pre-share
 encryption 3des
 hash md5
 group 2
 lifetime 86400
crypto isakmp am-disable
telnet timeout 5
ssh timeout 5
console timeout 0
dhcpd dns 205.171.3.65 205.171.2.65
dhcpd auto_config outside
!
dhcpd address 172.10.20.2-172.10.20.33 inside
dhcpd enable inside
!

!
class-map inspection_default
 match default-inspection-traffic
!
!
policy-map type inspect dns preset_dns_map
 parameters
  message-length maximum 512
policy-map global_policy
 class inspection_default
  inspect dns preset_dns_map
  inspect ftp
  inspect h323 h225
  inspect h323 ras
  inspect rsh
  inspect rtsp
  inspect esmtp
  inspect sqlnet
  inspect skinny
  inspect sunrpc
  inspect xdmcp
  inspect sip
  inspect netbios
  inspect tftp
!
service-policy global_policy global
group-policy DfltGrpPolicy attributes
 banner none
 wins-server none
 dns-server none
 dhcp-network-scope none
 vpn-access-hours none
 vpn-simultaneous-logins 3
 vpn-idle-timeout none
 vpn-session-timeout none
 vpn-filter none
 vpn-tunnel-protocol IPSec
 password-storage disable
 ip-comp disable
 re-xauth disable
 group-lock none
 pfs enable
 ipsec-udp disable
 ipsec-udp-port 10000
 split-tunnel-policy tunnelall
 split-tunnel-network-list none
 default-domain none
 split-dns none
 intercept-dhcp 255.255.255.255 disable
 secure-unit-authentication disable
 user-authentication disable
 user-authentication-idle-timeout 30
 ip-phone-bypass disable
 leap-bypass disable
 nem disable
 backup-servers keep-client-config
 msie-proxy server none
 msie-proxy method no-modify
 msie-proxy except-list none
 msie-proxy local-bypass disable
 nac disable
 nac-sq-period 300
 nac-reval-period 36000
 nac-default-acl none
 address-pools none
"""


class MockSsh(object):

    COMMANDS = {
        '': '', 'enable': 'password: ', 'terminal pager 0': '', 'disable': '', 'show run': sample_config, 'end': '',
        'show run hostname': 'test_hostname', 'write memory': 'written', 'config terminal': '',
        'show run route': "route outside 0 0 10.1.2.2 1/nroute inside 192.168.1.0 255.255.255.0 192.168.1.254 1",
        'route outside 192.168.1.0 255.255.255.0 192.168.0.254': '',
        'no route outside 192.168.1.0 255.255.255.0 192.168.0.254': ''
    }

    def __init__(self, hostname, username, password):
        self.hostname = hostname
        self.username = username
        self.password = password

    def send_command(self, command, results=True):
        return self.COMMANDS[command]

    def login(self):
        pass

    def is_logged_in(self):
        return True


