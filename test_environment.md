### test environment ###


**Illustration:**

```
   purty (br0)---------------------------------------------------------------------
                      |                      |               |           |         |
  purty ips         11.1                    12.1             |           |         |
                      |                      |               |           |         |
                     tap1                    tap2           tap0       tap3       tap4
                      |                      |               |           |         |
lennygwbox uplinks eth1 11.12             eth2 12.12         |           |         |
                      |                      |               |           |         |
                      |                      |               |           |         |
                      |                      |               |           |         |
lennybox "lan"        -----  eth0 0.12 ------                |           |         |
                                  |__________________________|           |         |
                                                                         |         |
                                                                         |         |
                               __________________________________________|         |
                              |                          __________________________|
                              |                          |
lan clients            alan (eth0_0.89) - tap3         blan (eth0 0.116) - tap4

```


```
ip addresses    abbreviation   description

192.168.11.1    11.1           purty, virtualbox host
192.168.12.1    12.1           purty, virtualbox host
192.168.11.12   11.12          lennygwbox, virtual, uplink1 facing
192.168.12.12   11.12          lennygwbox, virtual, uplink2 facing
192.168.0.12    0.12           lennygwbox, virtual, lanfacing
192.168.0.89    0.89           alan, lan client
192.168.0.116   0.116          blan, lan client
```


---


**description**

```
We have a virtualbox host machine purty (this is not the muggles box, but the machine hosting the virtual muggles box). Purty has:
  internet eth1_host (192.168.1.102)
  br0 (11.1, 12.1) under which: (tap0: 0.12, tap1: 11.1, tap2: 12.1, tap3 0.89, tap4 0.116)

Purty masquerades, forwarding stuff from br0 interface to eth1_host internet interface
```


```
We have a virtualbox client machine: lennygwbox (the muggles box)

  lennygwbox has purty as the gateway for its two gateway uplinks:
    (lennygwbox eth1 (192.168.11.12) --- dev tap1 -> hostgw (192.168.11.1) )
    (lennygwbox eth2 (192.168.12.12) --- dev tap2 -> hostgw (192.168.12.1) )

    (tap1 and tap2 are bound to br0)

  This virtualbox client machine lennygwbox also has an interface to the "lan", eth0 (0.12).

Clients we want to have using lennygwbox on this lan are alan and blan
  (alan and blan are also virtualbox clients of the virtualbox host).

If we allocated an ip like 0.1 to br0 then purty would masquerade alan and blan directly to the net (huh? fix/check)

  But, for simulation testing we want to masquerade them
    with forwards going from their lan interfaces 0.X
        to eth0 (0.12)
          to uplink1 eth1 11.12, or to uplink2 eth2 12.12 and thence further

  alan 0.89 -->tap3 -> 0.12 -> 11.12 or 12.12 -> etc
  blan 0.116 -->tap4 -> 0.12 -> 11.12 or 12.12 -> etc

  (tap0, tap3 and tap4 are bound to br0)

```


---



**Problem:**
lennybox can't see packets on eth0 (0.12) from alan (eth0 0.89) because ip packets from alan have no link to eth0 (mac frames do)

_layer 3 solution:_

We can give purty br0 another ip address (let's use 0.1) for (tap0,tap3,tap4) -> br0 connection. This makes subnet br0 work (for 192.168.0.x):
```
  ip addr add 192.168.0.1/24 dev br0
  ip route add 192.168.0.0/24 dev br0
```
It works, mostly, but it isn't really recommended because it doesn't really simulate what we want. We should instead use layer 2 processing.


_layer 2 solution_

The ip addressing allocation of the previous section solves the problem for layer 3 apps. But we shouldn't really have that bypass because:

  * it doesn't emulate the set up you want to simulate correctly (the bypass is like having a physical cable to let you go into the lanface where alan, blan and 0.12 are connected (see tap0, tap3, tap4) from a location that is upstream from the muggles box).

  * ipaudit and others rely on layer 2 tools like libpcap. But the ip address associated with the packets on the lanface gets the layer 3 ip bridge address bolted on under some circumstances (eg iptables set up with no -o options (this is usually wrong) for the MASQUERADE action on purty) rather than the originating lan client ip address. So, if alan sends a packet, the originating ip is seen as 0.1 rather than 0.89 by libpcap and ipaudit.

So it is better to use layer 2 stuff, and not have to allocate an ip address at all.

Ethernet frames _should_ be passing through, but default debian lenny has bridging filters in place. To disable them. we run this on purty:

```
#!/bin/bash
b="/proc/sys/net/bridge/bridge-nf-"

for i in $b'call-arptables' $b'call-ip6tables' $b'call-iptables' $b'filter-pppoe-tagged' $b'filter-vlan-tagged'
do echo 0 > $i
done
```

(for the current system you actually don't need to have -call-ip6tables and -filter-pppoe-tagged and -filter-vlan-tagged. Setting -call-iptables to zero means that during masquerading, the bridge interface will not respond claiming the ip unless the bridge interface really is bound to the ip (rather than merely one of the interfaces to the machine which has the ip bound to another interface). -call-arptables does the same for normal (non-masq) bridge interfaces. (that's my understanding - comments welcome)).


---


**Implementation**

OK, we have the background, let's implement it:

```
#!/bin/bash
set -x
set -v

brctl addbr br0

tap_last=5
for ((i=0; i<=$tap_last; i++)) ; do
 tunctl -t tap$i -u peej
 brctl addif br0 tap$i
 ifconfig tap$i up
done


ip addr add 192.168.11.1/24 dev br0
ip addr add 192.168.12.1/24 dev br0
ip link set br0 up

b="/proc/sys/net/bridge/bridge-nf-"
for i in $b'call-arptables' $b'call-iptables'
do echo 0 > $i
done


modprobe vboxdrv


function natup
{
#masq etc
#want to pass lanface (br0) and netface (eth1)
lanface=$1
netface=$2
echo 0 > /proc/sys/net/ipv4/conf/all/rp_filter
echo 1 > /proc/sys/net/ipv4/conf/all/arp_ignore

echo 1 > /proc/sys/net/ipv4/ip_forward

iptables -F

iptables -t nat -F
iptables -t mangle -F
iptables -X

# Always accept loopback traffic
iptables -A INPUT -i lo -j ACCEPT
iptables -A OUTPUT -o lo -j ACCEPT

#Allow established connections to this machine
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

#allow LAN to this machine
iptables -A INPUT -m state --state NEW -i $lanface -j ACCEPT

#Allow established forwards from internet to LAN
iptables -A FORWARD -i $netface -o $lanface -m state --state ESTABLISHED,RELATED -j ACCEPT

# Allow forwards from the LAN side. to the internet
iptables -A FORWARD -i $lanface -o $netface -j ACCEPT

#don't allow forwards from outside to LAN
iptables -A FORWARD -i $netface -o $lanface -j REJECT

#allow masq using internet interface
iptables -t nat -A POSTROUTING -o $netface -j MASQUERADE

return 0
}

natup "br0" "eth1"

```



Now, fire up your boxen (you'll have to prepare the images to taste):

```
vboxheadless -s lennybase
vboxheadless -s alanclient
vboxheadless -s blanclient
vboxheadless -s clanclient
```

to test stuff out.

Hints on making the images after you've made one client which you can clone:

```
vboxmanage clonevdi alanclient.vdi dlanclient.vdi
```
(make sure alanclient.vdi is powered off)

```
vboxmanage registerimage disk dlanclient.vdi
vboxmanage createvm -name dlanclient
```

do a comparison between vboxmanage showvminfo dlanclient and vboxmanage showvminfo alanclient, and modify acordingly,
eg:
```
vboxmanage modifyvm dlanclient -ostype Debian -memory 512MB
```

Actually, I've managed to have the lanclients run with a minimal install of 32MB. You should be able to get the diskspace with the lanclients to less than 1 GB.

For the lennygwbox image I used up 256 MB of RAM. It can probably run without a glitch in 64MB for testing purposes.

Things to change on a new client: nic, hostname?