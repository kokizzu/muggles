## /etc/network/interfaces ##

To keep it simple, we assume one IP address per interface.

> (i) For lan-facing default eth0, use a static ip, set address to lan ip of gatewaybox itself, add netmask, (gateway, broadcast is optional, choice of auto or allow-hotplug is optional for eth and depends on if your nic has plugging detection). (note: /etc/network/if-up.d/masq\_ipconf and /etc/dnsmasq.conf use eth0 hardcoded as lan facing interface.)

> Default nameservers are set in this order: dnsmasq, google public dns, opendns (opendns will give you a search page if the domain does not exist. With luck that should never happen). You may want to use your ISP's nameserver instead of the google or opendns nameserver.


> (ii) For each extra uplink interface:

> add each interface used to the allow-hotplug line, and

> follow the pattern of uplink2 (iface eth2...) (don't follow the pattern of uplink1, which has an extra line adding a default gateway for the muggles box itself. I should probably factor that out later).

> If you follow that pattern, then each uplink interface will add an uplink1, uplink2, uplink2... routing table in iproute2/rt\_tables. These will use 10, 20, 30... for the serial numbers. Which means 25 uplink interfaces at most. No check is done for if the serial number is already taken by another label. Should code that and put a limit too. Later. Also rt\_tables uplink removal is not done. Should it be done?

> (iii) each uplink interface runs masq\_ip.conf from `/etc/network/if-pre-up.d`. This sets up firewalling, forwarding and masquerading using iptables and /proc/sys/net/ipv4 settings. (Squid (if used) would need to be detected as running first before lan machines are redirected to to squid using iptables. Squid detection and possible redirection is done separately, later, in /etc/init.d/mugglesinit)