### other scripts ###

**/usr/local/sbin/**

  * rulerunner - select random or roundrobin as distribution method for rules (configuration is in /etc/muggles/rulerunner.conf (and forced\_uplink.conf)
  * defaultrouting - rotates between uplinks for a default route for the muggles box if a link goes down. Really needed to ensure router is always able to resolve stuff. Also has routing set for ping to uplink destinations pinged from muggles box.
  * pinglogger - reachability logger. Has a configuration file in /etc/muggles/pinglogger.conf

> If you install ipaudit, it also places ipstrings and ipaudit in /usr/local/sbin/.

**/usr/lib/cgi-bin**

  * showcurrent.cgi is the main web display script. Configuration is in /etc/muggles/showcurrent.conf
  * switchisps.cgi is another major one which shifts users to another uplink.
  * machine\_settings.cgi allows
    * switching squid cache usage on or off for a machine on the lan.
    * forcing a particular uplink to be used for a machine on the lan.
  * there are more

**/etc/init.d/mugglesinit**
Initializes stuff at start up:
  * sets up iptables redirection for transparent squid (if squid is up)
  * polls if all the interfaces are up (timing out if necessary)
  * gets the default routing and route monitoring system going for the muggles box
  * does a time sync with ntp servers
  * initializes stuff for rulerunner
  * does an aptitude update and puts the packages-to-upgrade list up
  * starts pinglogger

> It has a verbosity switch in the code if you want to see what is going on (useful for checking race conditions and profiling a bit).