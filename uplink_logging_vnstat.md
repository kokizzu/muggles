### vnstat configuration ###

**set it up**

```
aptitude install vnstat
```

If you have two uplinks, eth1 and eth2, then initialize their databases with:

```
vnstat -u -i eth1
vnstat -u -i eth2
```

That's all. (A cronjob /etc/cron.d/vnstat runs a vnstat update every 5 minutes by default. If you shut the machine down you can therefore lose up to 5 minutes of data. That's probably ok for most people. If it isn't ok for you, then a workaround is to script a vnstat -u on shutdown for each interface).

**To see it in action:**

Point your browser at http://192.168.0.12/cgi-bin/showcurrent.cgi (or whatever you use as your muggle box ip when accessing it from the LAN).

Move your mouse pointer over where it says isp1 or isp2 on the main web page. By default you see the monthly statistics as hovertext.

**to customize it**

To modify the hovertext, you'll need to modify the vnstat section in the showcurrent.cgi code.

Examples of possible modifications

> vnstat -d -i eth1 - daily use on uplink1

> vnstat -h -i eth2 - hourly use on uplink2

> vnstat -m -i eth2 - monthly use on uplink2

man(1) vnstat has lots more options.