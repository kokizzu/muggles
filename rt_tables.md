### /etc/iproute2/rt\_tables ###

For each uplink, the /etc/network/interfaces file adds a line to this file. Eg for three uplinks, have:

```
10      uplink1
20      uplink2
30      uplink3
```

This is done automatically based on /etc/network/interfaces settings, so you don't need to do anything. Once set it is also persistent, which may not be neat, but should not be a problem.