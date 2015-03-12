### /var/log/muggles/ ###

Under here we have:

  * lease\_and\_rulechanges.log tracks rulerunner runs and machine\_settings.cgi runs that affect leases and rules. (You can switch it off by setting logon=0 in /etc/muggles/rulerunner.conf)
  * remote\_pings.log logs remote connectivity via an interface. (pinglogger generated) (used by web gui)
  * near\_pings.log logs near connectivity via an interface. (pinglogger generated) (used by web gui)
  * secupdates tracks if any updates exist for the host OS (these will be mostly security updates) (used by web gui)

Logrotate handles all 