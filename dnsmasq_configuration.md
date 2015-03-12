### /etc/dnsmasq.conf ###

With this file we can set things like:

  * the interface (eth0 by default)
  * dhcp-range (eg: 192.168.0.50 to 192.168.0.150)
  * dns servers and timeservers that you want the machines on the lan to use.

Mostly however you'll be changing mac addresses each time you decide a machine should be allowed to make use of the lan.

This (mac addresses and host names of machines on the lan) can be done in the "dhcp-host" bit , but to keep things simple I suggest you use /etc/ethers instead (like the installscript does).

setting mac address with host names sets host name for each interface in the dnsmasq nameserver. So everyone on lan using the service can refer to it. Each ip is assigned dynamically for the client, and held in /var/lib/misc/dnsmasq.leases.

Bear in mind that standard dhcp is not proof against spoofing-IP-hijacking, which can lead to strangeness if someone is being evil on the lan. To be secure against that (eg if you are in a bank setting where you should be paranoid), set up wpa with psk or similar.

Hint: to see all the non-default lines in dnsmasq.conf, do a "grep -v ^# /etc/dnsmasq.conf | grep ."

If you change the other automatically enabled options (dns options, routers, and timeserver, you should do that by adjusting it in dnsmasq.conf and reloading dnsmasq (/etc/init.d/dnsmasq restart).

If the dhcp-range has the ip address of the dhcp-server inside the range, it is not a problem. dnsmasq is smart that way. So the installscript doesn't bother to check for that. The only issue is that the range will then have one less address available (if the ip of the dhcpserver is inside that range), which may be a little confusing if you aren't aware of it.