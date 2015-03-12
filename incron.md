### inotify and incron to monitor dnsmasq lease changes ###

We want to monitor the dnsmasq leases file, because whenever it changes it means a machine has dhcp-joined or dhcp-left the LAN. When a machine has joined we add routing rules for it which decide which uplink it gets to use. When it leaves, we remove its rule. The rules are run from the imaginatively-named rulerunner script.

A machine may leave the lan without informing it has left. That's ok, dhcp allows for that, even though it doesn't specifically know if the machine is there or not. For an admin it is useful to know if a machine is on the lan or not - the web gui (discussed in another section) shows that at a glance using ping diagnostics.

Anyway, back to monitoring dnsmasq leases. To set  monitoring up, we first find where dnsmasq keeps its lease file. In Lenny it's at /var/lib/misc/dnsmasq.leases, unless otherwise defined in dnsmasq.conf. Running these 3 lines in your bash shell should tell you where it is:

```
  leasefile=`( grep -v ^# /etc/dnsmasq.conf | grep dhcp-leasefile ) | cut -f2 -d=`
  if [ -z "$leasefile" ] ; then leasefile="/var/lib/misc/dnsmasq.leases" ; fi
  echo $leasefile
```

Whereever it is, we want inotify to monitor it for changes. Incron lets us do it like this:

#incrontab -e:
/var/lib/misc/dnsmasq.leases IN\_MODIFY,IN\_NO\_LOOP /usr/local/sbin/rulerunner $@

To make incron work for root, add the word root in /etc/incron.allow
(For convenience you may want to set editor to vi in /etc/incron.conf)

Incrontab has some problems with whitespace in the lenny version which makes it hard to use extensively with other entries.