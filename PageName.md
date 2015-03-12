
# Introduction #

## Quickstart (for typical 2-uplinks, serving 1 LAN case) ##

### The setup ###

Assuming you have 3 ethernet cards on your gateway box.

  * eth0 faces your lan,  and is 192.168.0.12 by default.
  * eth1 is your uplink1, and is 192.168.11.12 by default.
  * eth2 is your uplink2, and is 192.168.12.12 by default.

also:

  * alan is one machine on the lan by default
  * blan is another machine on the lan by default


In pictures:

```
     T H E   I N T E R N E T  
          |         |
        uplink1  uplink2
          |        |
         ______________
         | gatewaybox |
         --------------
               |
            lanlink
               |
        --------------------------
       |            |        |
     alan         blan

```

### The install ###

The 8-fold path to a higher uplink state...

1. Install lenny with a minimal bunch of packages (no x needed).

  * With the debian-503-i386-netinst.iso, when it detects the network interfaces chose any one as the primary, but keep the interfaces physically disconnected. Let it try to dhcp and fail, then choose "do not configure network at this time". Kind of silly, but keeps it simple.

  * When it prompts you for package selection near the end of the installation, you can drop the selection "standard" so that it is truly a minimal installation.

2. Unpack the tgz file in, say /root/muggles\_source.

3. To install, run ./installscript.

4. Enter the static ip addresses for the lan, uplinks, and gateways at the prompts.

5. Change/add mac addresses of the lan machines in /etc/ethers (Replace alan, blan etc.)

6. Connect up alan (or rather, its replacement). You already entered the mac address for this machine in the previous step. If you have a normal modern OS, then the machine will simply auto-configure and get its network; dns and time settings from the muggles box.

7. Then point your browser to http://192.168.0.12 (or whatever you've changed the muggles box ip address to in step 4)

8. admire the pre-millennial web interface

You should have now have a basic muggles with web gui front end. It does web and dns caching; time serving; checks for lenny updates; informs you of monthly use per uplink; lets you know what machines are alive on the lan; and checks and lets you change your uplinks from the web gui.

If your setup is more complicated, you can adjust the configuration files in /etc/muggles/ and the config files of the other components. You can read up on the details in the section below:

## Not-so-Quickstart (for if you want to dig in) ##


### The Details ###

(this is roughly in order of dependency and logic).

A `*` tags the areas that the install script may change.

[/etc/network/interfaces](http://code.google.com/p/muggles/wiki/interfaces) `*`

[/etc/iproute/rt\_tables](http://code.google.com/p/muggles/wiki/rt_tables) `*`

[dnsmasq configuration](http://code.google.com/p/muggles/wiki/dnsmasq_configuration) `*`

[incron](incron.md) `*`

[/usr/local/sbin/rulerunner](http://code.google.com/p/muggles/wiki/rulerunner) `*`

[/var/log/muggles/](var_log_muggles.md) `*`

[/etc/muggles](muggles.md) `*`

[/etc/lighttpd.conf](lighttpd.md) `*`

[other scripts](other_scripts.md) `*`

[/etc/sudoers](sudoers.md) `*`

[uplink logging: bandwidthd](uplink_logging_bandwidthd.md)

[uplink logging: vnstat](uplink_logging_vnstat.md) `*`

[uplink logging: darkstat](uplink_logging_darkstat.md)

[squid](squid.md) `*`

[ipaudit](ipaudit.md) (recommended)

[logrotate](logrotate.md) `*`

[openssh client and server](openssh.md) `*`

[test environment](test_environment.md)