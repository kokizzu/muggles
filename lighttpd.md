### /etc/lighttpd.conf ###

> (i) enable cgi module by using command "lighty-enable-mod cgi", and reload lighty: /etc/init.d/lighttpd restart

> (ii) append own bits to lighttpd.conf with our own lanfacing (eth0) ip.address (defined in interfaces, or dig out the value with `ip -4 -o addr show dev eth0 | sed -n 's/^.*inet \(.*\)\/.*$/\1/p'`. We append the following bits (to tweak cgi settings) to the default lenny lighttpd.conf file (then reload lighty):
```
## Adding our bits now.
## Here we enable cgi for anyone accessing this ip (mod-cgi default only enables for access from 127:1)
## remoteip = ip address of browser, host = hostname in url requested

$HTTP["host"] =~ "192.168.0.12" {
        alias.url += (
                "/cgi-bin/" => "/usr/lib/cgi-bin/"
        )
        $HTTP["url"] =~ "^/cgi-bin/" {
                cgi.assign = ( "" => "" )
        }
}
```
Consider removing access to /usr/share and images, and dir listing from default lenny

> (iii) We can further append the following to serve ipaudit (remember to reload lighty).
```
## ipaudit bits
$HTTP["host"] =~ "192.168.0.12" {
        alias.url += (
                "/~ipaudit/cgi-bin/" => "/home/ipaudit/public_html/cgi-bin/",
                "/~ipaudit/images/" => "/home/ipaudit/public_html/images/"
        )
        $HTTP["url"] =~ "^/~ipaudit/cgi-bin/" {
                cgi.assign = ( "" => "" )
        }
}
```