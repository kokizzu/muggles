### /etc/muggles ###

**/etc/muggles/ has configuration files under it:**

  * rulerunner.conf (configuration options to decide rule assignment for machines, sourced by machine\_settings.cgi, mixed and rulerunner)
  * pinglogger.conf (sourced by pinglogger, defaultrouting and showcurrent.conf)
  * showcurrent.conf (sourced by showcurrent.cgi)
  * forced\_uplink.conf (sourced by machine\_settings.cgi and rulerunner - forces machine to a particular gateway)

**Not done under /etc/muggles/:**

  * dhcp's mac-machine settings are currently primarily set in /etc/dnsmasq.conf (though /etc/network/interfaces steps in if some settings don't exist).

  * rt\_tables are decided by /etc/network/interfaces rt\_tables in the uplinks section