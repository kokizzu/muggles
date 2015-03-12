### darkstat ###

Another bolt on utility.

  * Set the interface to the one you want to monitor in /etc/darkstat/init.cfg, eg:
```
INTERFACE="-i eth0"
```

  * Turn it on by setting the toggle in /etc/darkstat/init.cfg on, eg:
```
START_DARKSTAT=yes
```

(Re)start it with /etc/init.d/darkstat start.

Browse http://192.168.0.12:667  (or use whatever web ip is appropriate)

It's neat, but not really that useful for muggles. I'm just documenting how to set it up here as a quick note in case someone finds it handy for their own purposes.