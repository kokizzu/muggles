### squid configuration ###

For transparent web proxy caching with lenny's squid 2.7stable3 :

In (network section of) /etc/squid.conf set:

```
  http_port 127.0.0.1:3128 transparent
  http_port 192.168.0.12:3128 transparent
  visible_hostname lennygwbox.local
```

To make visible\_hostname work add lennygwbox.local in /etc/hosts to the line 127.0.0.1 like:
```
  127.0.0.1       localhost       lennygwbox.local 
```

In (acl section of) /etc/squid.conf set:

```
  acl our_networks src 192.168.0.0/24
  http_access allow our_networks
```


If squid is running, and we want pull out possible web caches from it, then we want to run a proxy redirect on the muggles box:

```
  iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 80 -j REDIRECT --to-port 3128
```

This is dnat - the destination everything goes to is changed. This happens in the redirect action for the chain before routing. The action sends packets to port 3128, to squid. It happens without the client knowing about it, which is why it is called transparent proxying. (In normal proxying you usually set http\_proxy or such on your client).

(You can contrast this with snat - where the source everything originates from is changed. This happens in the masquerade action for the chain after routing. The action rewrites packets so that they look like they originate from the muggles box. Snat is how muggles is set up at all times, whether or not squid is running).

The iptables line should only be run after squid is detected. Since squid only runs after sometime after the interfaces are up (see rc2.d scripts) we can't put it in the interfaces script and neatly detect squid later on. So we put the line in mugglesinit and make sure it runs after squid is up. That's a one-shot afair. Turn off squid, and you have to delete the iptables entry. So:


To stop squid:

```
   lennygwbox:~# /etc/init.d/squid stop && iptables -t nat -D PREROUTING -i eth0 -p tcp --dport 80 -j REDIRECT --to-port 3128
   Stopping Squid HTTP proxy: squid Waiting.....................done.
```

To start it up again:
```
   lennygwbox:~# /etc/init.d/squid start && iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 80 -j REDIRECT --to-port 3128
   Starting Squid HTTP proxy: squid.
```

The web GUI lets you click on a machine name and turn off its squid use. This may be useful for web developers who want to bypass caching issues. This setting is lost on reboot of the muggles router.