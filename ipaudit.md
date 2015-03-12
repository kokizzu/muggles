### ipaudit ###


Extensive ip auditing. Logs each connection. Not part of the default install.

It isn't a debian package, and is getting on the edge of being unmaintained. But it is such a good tool, and works so well with muggles, that here's the recipe to install it. It's quite easy for... um... people who find it easy:


For lenny:

  * get the tar.gz packages:
```
wget http://downloads.sourceforge.net/project/ipaudit/ipaudit-web/ipaudit-web-1.0BETA9/ipaudit-web-1.0BETA9.tar.gz
wget http://downloads.sourceforge.net/project/ipaudit/ipaudit/ipaudit-1.0/ipaudit-1.0rc9.tar.gz
```

  * get other packages needed:
```
aptitude install make gcc libpcap0.8 libpcap0.8-dev gnuplot 
```

  * unpack ipaudit`*`.tar.tgz files, and follow prompts on ./configure -> make etc

  * when prompted to add user ipaudit:
```
  adduser ipaudit
```

  * set ipaudit.conf file localrange:  `LOCALRANGE=192.168.0.0/24`

  * set ipaudit.conf file interface: `INTERFACE=eth0`
> > ( We won't monitor the uplinks. Those will be handled with vnstat or bandwidthd instead )

  * symlink these paths:
```
ln -s /var/www/ipaudit /home/ipaudit/public_html
ln -s '/var/www/~ipaudit' /home/ipaudit/public_html
```

  * Dare we do this?:
```
chgrp www-data /home/ipaudit/ipaudit-web.conf
```
> > Yes we dare! It is read only after all.


  * Adjust [/etc/lighttpd.conf](lighttpd.md) to handle ipaudit urls.

Now point your browser at http://192.168.0.12/ipaudit  (or whatever the webserver ip is). The cronjobs for ipaudit will accumulate the lan data, and resolve and build up pretty graphs that you can click your way through.