### bandwidthd ###

This shows daily/weekly/monthly bandwidth usage with pretty graphs.

You just bolt it in:

Install with "aptitude install bandwidthd", and select "any" as the interface. /etc/bandwidthd/bandwidthd.conf for the default ips will then have these settings:

```
  subnet 192.168.0.0/24
  subnet 192.168.12.0/24
  subnet 192.168.11.0/24

  dev "any"
```

Make a symlink: ln -s /var/lib/bandwidthd/htdocs/ /var/www/bandwidthd

To see bandwidth usage, you point your browser at http://192.168.0.12/bandwidthd (or whatever your host address is after you had set it in /etc/network/interfaces).

Bandwidthd it is pretty much the same as vnstat, except it has web display. I prefer vnstat overall because you can work the statistics with scripts easier and then show only the information you are really interested in in the web gui.