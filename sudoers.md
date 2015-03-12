### /etc/sudoers ###

If the box has a hostname of lennygwbox, then the /etc/sudoers file has these entries:

```
www-data        lennygwbox= NOPASSWD: /sbin/shutdown
www-data        lennygwbox= NOPASSWD: /sbin/ip
www-data        lennygwbox= NOPASSWD: /usr/bin/nmap
www-data        lennygwbox= NOPASSWD: /usr/local/sbin/mixed
```

They allows web gui scripts to work with root privileges.

Note that the default allows anyone on the lan to shut the system down. This is often a feature.