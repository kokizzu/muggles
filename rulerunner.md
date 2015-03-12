### /usr/local/sbin/rulerunner ###

Changes in dnsmasq.leases are detected by inotify, which invokes the rulerunner script.

The rulerunner script adds and deletes rules based on the dnsmasq.leases file changes.

In the rc scripts for lenny, dnsmasq starts before incron in the rc2 S level. So if dnsmasq.leases file changes are already done, then incron will not notice them. So for robustness, we run a dnsmasq.leases check using init.d/mugglesinit. Squeeze has a similar race condition with dnsmasq and incron actually at the same S level.
S and K levels are heading for obsolescence anyway, so the init script has dependency booting definitions that will handle the sequence in future.

If we want to force specific machines to stick to a particular uplink you use /etc/muggles/forced\_uplink.conf.